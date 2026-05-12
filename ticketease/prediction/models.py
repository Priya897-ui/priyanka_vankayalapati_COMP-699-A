from django.db import models
from tickets.models import Ticket


class Prediction(models.Model):

    # Link to ticket
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)

    # ML Outputs
    success_probability = models.FloatField()
    risk_index = models.FloatField()

    # Decision Output
    recommendation = models.CharField(max_length=50)

    # Explanation (for user understanding)
    explanation = models.TextField(blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction for Ticket {self.ticket.id}"