from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'license_number',
        'phone',
        'past_violations',
        'accident_history',
        'created_at'
    )

    search_fields = ('user__username', 'license_number', 'phone')


admin.site.register(Profile, ProfileAdmin)