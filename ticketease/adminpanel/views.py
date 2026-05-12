from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from tickets.models import Ticket
from prediction.models import Prediction
from reminders.models import Reminder


# ---------------------------------------
# Admin Dashboard
# ---------------------------------------
@staff_member_required
def admin_dashboard_view(request):

    total_tickets = Ticket.objects.count()
    total_predictions = Prediction.objects.count()
    total_reminders = Reminder.objects.count()

    context = {
        'total_tickets': total_tickets,
        'total_predictions': total_predictions,
        'total_reminders': total_reminders
    }

    return render(request, 'dashboard.html', context)


# ---------------------------------------
# OCR Logs (Simulated)
# ---------------------------------------
@staff_member_required
def ocr_logs_view(request):

    tickets = Ticket.objects.filter(processed=True)

    context = {
        'tickets': tickets
    }

    return render(request, 'cases.html', context)


# ---------------------------------------
# ML Logs (Prediction Monitoring)
# ---------------------------------------
@staff_member_required
def ml_logs_view(request):

    predictions = Prediction.objects.all().order_by('-created_at')

    context = {
        'predictions': predictions
    }

    return render(request, 'cases.html', context)


# ---------------------------------------
# System Report Summary
# ---------------------------------------
@staff_member_required
def report_view(request):

    total_tickets = Ticket.objects.count()
    contested = Prediction.objects.filter(recommendation="Contest Ticket").count()
    paid = Prediction.objects.filter(recommendation="Pay Fine").count()

    context = {
        'total_tickets': total_tickets,
        'contested': contested,
        'paid': paid
    }

    return render(request, 'dashboard.html', context)