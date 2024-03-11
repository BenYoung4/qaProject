import random
import string
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import get_user_model
from .form import CreateTicketForm, AssignTicketForm
from .models import Ticket

User = get_user_model()


# Creates ticket
def generate_unique_ticket_id():
    while True:
        id = ''.join(random.choices(string.digits, k=6))
        if not Ticket.objects.filter(ticket_id=id).exists():
            return id

def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.customer = request.user
            ticket.ticket_id = generate_unique_ticket_id()
            ticket.save()
            messages.success(request,
                             'Your ticket has been submitted. A helpdesk agent will reach out soon.')
            return redirect('customer-active-tickets')
        else:
            messages.warning(request, 'Something went wrong. Please check form errors')
            return redirect('create-ticket')
    else:
        form = CreateTicketForm()
        context = {'form': form}
        return render(request, 'tickets/create_ticket.html', context)


# View active tickets
def get_tickets(request, role, is_resolved, template_name):
    if role == 'helpdesk':
        filter_params = {'is_resolved': is_resolved}  # remove the role filter
    else:
        filter_params = {role: request.user, 'is_resolved': is_resolved}

    tickets = Ticket.objects.filter(**filter_params).order_by('-created_on')

    context = {'tickets': tickets}
    return render(request, template_name, context)


def customer_active_tickets(request):
    return get_tickets(request, 'customer', False, 'tickets/customer_active_tickets.html')


def customer_resolved_tickets(request):
    return get_tickets(request, 'customer', True, 'tickets/customer_resolved_tickets.html')


def helpdesk_active_tickets(request):
    return get_tickets(request, 'helpdesk', False, 'tickets/helpdesk_active_tickets.html')


def helpdesk_resolved_tickets(request):
    return get_tickets(request, 'helpdesk', True, 'tickets/helpdesk_resolved_tickets.html')


# Assign tickets to helpdesk agent
def assign_ticket(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    if request.method == 'POST':
        form = AssignTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_assigned_to_helpdesk = True
            var.status = 'Active'
            var.save()
            messages.success(request, f'Ticket has been assigned to {var.helpdesk}')
            return redirect('ticket-queue')
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
            return redirect('assign-ticket')  # check this out later
    else:
        form = AssignTicketForm(instance=ticket)
        form.fields['helpdesk'].queryset = User.objects.filter(is_helpdesk=True)
        context = {'form': form, 'ticket': ticket}
        return render(request, 'tickets/assign_ticket.html', context)


# View ticket details
def ticket_details(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    context = {'ticket': ticket}
    return render(request, 'tickets/ticket_details.html', context)


# View ticket queue is user is admin
def ticket_queue(request):
    tickets = Ticket.objects.filter(is_assigned_to_helpdesk=False)
    context = {'tickets': tickets}
    return render(request, 'tickets/ticket_queue.html', context)


def resolve_ticket(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    if request.method == 'POST':
        rs = request.POST.get('rs')
        ticket.resolution_steps = rs
        ticket.is_resolved = True
        ticket.status = 'Resolved'
        ticket.save()
        messages.success(request, 'Ticket is now resolved and closed')
        return redirect('dashboard')
