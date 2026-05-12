from datetime import date
from django.utils import timezone
from .models import Reminder


# ---------------------------------------
# Check and Process Due Reminders
# ---------------------------------------
def process_due_reminders():
    """
    Find reminders due today or earlier and mark them as sent.
    Returns count of processed reminders.
    """

    today = date.today()

    due_reminders = Reminder.objects.filter(
        reminder_date__lte=today,
        is_sent=False
    )

    processed_count = 0

    for reminder in due_reminders:
        send_reminder(reminder)
        processed_count += 1

    return processed_count


# ---------------------------------------
# Simulated Send Reminder
# ---------------------------------------
def send_reminder(reminder):
    """
    Simulate sending reminder (console print for demo)
    """

    message = reminder.message or f"Reminder: Your ticket #{reminder.ticket.id} is due."

    # Simulate notification (console output)
    print(f"[REMINDER SENT] User: {reminder.user.username} | {message}")

    # Mark as sent
    reminder.is_sent = True
    reminder.save()


# ---------------------------------------
# Utility: Manual Trigger (for demo)
# ---------------------------------------
def run_scheduler():
    """
    Manual trigger function (can be called from view or shell)
    """

    count = process_due_reminders()

    print(f"[SCHEDULER] Processed {count} reminders.")

    return count