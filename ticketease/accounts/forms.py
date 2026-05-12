from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile


# -----------------------------
# User Registration Form
# -----------------------------
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    # Driver info
    license_number = forms.CharField(max_length=50, required=False)
    phone = forms.CharField(max_length=15, required=False)

    # Driving history
    past_violations = forms.IntegerField(min_value=0, required=False, initial=0)
    accident_history = forms.IntegerField(min_value=0, required=False, initial=0)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            # ✅ IMPORTANT: DO NOT CREATE PROFILE
            # Just update profile created by signals.py

            profile = user.profile  # already created by signal

            profile.license_number = self.cleaned_data.get('license_number')
            profile.phone = self.cleaned_data.get('phone')
            profile.past_violations = self.cleaned_data.get('past_violations') or 0
            profile.accident_history = self.cleaned_data.get('accident_history') or 0

            profile.save()

        return user


# -----------------------------
# Login Form
# -----------------------------
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput)