from django.db import models
from django.contrib.auth.models import User
from tickets.models import Ticket


class Reminder(models.Model):

    # Link to user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Link to ticket
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)

    # Reminder details
    reminder_date = models.DateField()
    message = models.CharField(max_length=255, blank=True)

    # Status tracking
    is_sent = models.BooleanField(default=False)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reminder for Ticket {self.ticket.id} - {self.user.username}"