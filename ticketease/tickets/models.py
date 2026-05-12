from django.db import models
from django.contrib.auth.models import User


class Ticket(models.Model):

    # Link to user (Driver)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Basic ticket details (from simulated OCR)
    violation_type = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    fine_amount = models.FloatField()
    ticket_date = models.DateField()

    # Optional user input corrections
    is_edited = models.BooleanField(default=False)

    # Processing fields
    extracted_text = models.TextField(blank=True)
    processed = models.BooleanField(default=False)

    # Results (filled after prediction)
    success_probability = models.FloatField(null=True, blank=True)
    risk_index = models.FloatField(null=True, blank=True)
    recommendation = models.CharField(max_length=50, blank=True)

    # Case management
    is_saved = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.violation_type}"