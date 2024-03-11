from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tickets.models import Ticket

def get_context(user, resolved_status):
    tickets_filter = Ticket.objects.filter(customer=user, is_resolved=resolved_status) if user.is_customer else Ticket.objects.filter(is_resolved=resolved_status)
    return tickets_filter.count()

@login_required
def dashboard(request):
    user = request.user
    if user.is_customer or user.is_helpdesk:
        dashboard_type = 'customer_dashboard.html' if user.is_customer else 'helpdesk_dashboard.html'
        tickets_count = get_context(user, False)
        active_tickets_count = get_context(user, False)
        closed_tickets_count = get_context(user, True)
        context = {
            'tickets': tickets_count,
            'active_tickets': active_tickets_count,
            'closed_tickets': closed_tickets_count
        }
        return render(request, f'dashboard/{dashboard_type}', context)
    elif user.is_superuser:
        return render(request, 'dashboard/admin_dashboard.html')


def home_view(request):
    return render(request, 'home.html')
