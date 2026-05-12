from django.contrib import admin
from .models import Reminder


class ReminderAdmin(admin.ModelAdmin):

    # Columns displayed in admin panel
    list_display = (
        'id',
        'user',
        'ticket',
        'reminder_date',
        'is_sent',
        'created_at'
    )

    # Filters
    list_filter = (
        'is_sent',
        'reminder_date'
    )

    # Search fields
    search_fields = (
        'user__username',
        'ticket__id'
    )

    # Read-only fields
    readonly_fields = (
        'created_at',
    )


# Register model
admin.site.register(Reminder, ReminderAdmin)