from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

from .models import Reminder
from .scheduler import run_scheduler
from tickets.models import Ticket


# ---------------------------------------
# Create / Set Reminder
# ---------------------------------------
@login_required
def set_reminder_view(request, ticket_id):

    # Get ticket for current user
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == 'POST':
        try:
            reminder_date = request.POST.get('reminder_date')
            message = request.POST.get('message')

            # Convert date safely
            reminder_date = datetime.strptime(reminder_date, "%Y-%m-%d").date()

            # Create or update reminder
            Reminder.objects.update_or_create(
                ticket=ticket,
                defaults={
                    'user': request.user,
                    'reminder_date': reminder_date,
                    'message': message
                }
            )

            messages.success(request, "Reminder set successfully.")
            return redirect('/reminders/list/')

        except Exception as e:
            messages.error(request, f"Error setting reminder: {str(e)}")
            return redirect('/tickets/cases/')

    # ✅ IMPORTANT FIX → use separate template
    return render(request, 'set_reminder.html', {'ticket': ticket})


# ---------------------------------------
# View All Reminders
# ---------------------------------------
@login_required
def reminder_list_view(request):

    reminders = Reminder.objects.filter(user=request.user).order_by('reminder_date')

    return render(request, 'reminders_list.html', {'reminders': reminders})


# ---------------------------------------
# Trigger Scheduler (Manual Demo)
# ---------------------------------------
@login_required
def run_scheduler_view(request):

    count = run_scheduler()

    messages.success(request, f"{count} reminders processed.")

    return redirect('/reminders/list/')