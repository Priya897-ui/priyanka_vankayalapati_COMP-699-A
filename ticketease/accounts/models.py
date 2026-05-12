from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Driver-related fields (for ML input later)
    license_number = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=15, blank=True)

    # Driving history factors
    past_violations = models.IntegerField(default=0)
    accident_history = models.IntegerField(default=0)

    # Meta info
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username