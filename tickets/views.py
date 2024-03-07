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


# cx can create a ticket from here
def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.customer = request.user
            while not var.ticket_id:
                id = ''.join(random.choices(string.digits, k=6))
                try:
                    var.ticket_id = id
                    var.save()
                    # send email func
                    subject = f'{var.ticket_title} #{var.ticket_id}'
                    message = 'Thank you for creating a ticket, we will assign an engineer soon.'
                    email_from = 'benyoung@email.com'
                    recipient_list = [request.user.email, ]
                    send_mail(subject, message, email_from, recipient_list)
                    messages.success(request,
                                     'Your ticket has been submitted. A Support Engineer would reach out soon.')
                    return redirect('customer-active-tickets')
                    # break
                except IntegrityError:
                    continue
        else:
            messages.warning(request, 'Something went wrong. Please check form errors')
            return redirect('create-ticket')
    else:
        form = CreateTicketForm()
        context = {'form': form}
        return render(request, 'tickets/create_ticket.html', context)


# cx can see all active tickets
def customer_active_tickets(request):
    tickets = Ticket.objects.filter(customer=request.user, is_resolved=False).order_by('-created_on')
    context = {'tickets': tickets}
    return render(request, 'tickets/customer_active_tickets.html', context)


# cx can see all resolved tickets
def customer_resolved_tickets(request):
    tickets = Ticket.objects.filter(customer=request.user, is_resolved=True).order_by('-created_on')
    context = {'tickets': tickets}
    return render(request, 'tickets/customer_resolved_tickets.html', context)


# engineer can see all his/her active tickets
def engineer_active_tickets(request):
    tickets = Ticket.objects.filter(engineer=request.user, is_resolved=False).order_by('-created_on')
    context = {'tickets': tickets}
    return render(request, 'tickets/engineer_active_tickets.html', context)


# engineer can see all his/her resolved tickets
def engineer_resolved_tickets(request):
    tickets = Ticket.objects.filter(engineer=request.user, is_resolved=True).order_by('-created_on')
    context = {'tickets': tickets}
    return render(request, 'tickets/engineer_resolved_tickets.html', context)


# assign tickets to engineers
def assign_ticket(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    if request.method == 'POST':
        form = AssignTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_assigned_to_engineer = True
            var.status = 'Active'
            var.save()
            messages.success(request, f'Ticket has been assigned to {var.engineer}')
            return redirect('ticket-queue')
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
            return redirect('assign-ticket')  # check this out later
    else:
        form = AssignTicketForm(instance=ticket)
        form.fields['engineer'].queryset = User.objects.filter(is_engineer=True)
        context = {'form': form, 'ticket': ticket}
        return render(request, 'tickets/assign_ticket.html', context)


# ticket details
def ticket_details(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    context = {'ticket': ticket}
    return render(request, 'tickets/ticket_details.html', context)


# ticket queue (for only admins)
def ticket_queue(request):
    tickets = Ticket.objects.filter(is_assigned_to_engineer=False)
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
