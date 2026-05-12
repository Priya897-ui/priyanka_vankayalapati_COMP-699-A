from django.contrib import admin
from .models import Ticket


class TicketAdmin(admin.ModelAdmin):

    # Columns shown in admin table
    list_display = (
        'id',
        'user',
        'violation_type',
        'location',
        'fine_amount',
        'ticket_date',
        'success_probability',
        'risk_index',
        'recommendation',
        'processed',
        'created_at'
    )

    # Filters on right side
    list_filter = (
        'violation_type',
        'processed',
        'ticket_date'
    )

    # Search functionality
    search_fields = (
        'user__username',
        'location',
        'violation_type'
    )

    # Read-only fields (important for system integrity)
    readonly_fields = (
        'extracted_text',
        'processed',
        'success_probability',
        'risk_index',
        'recommendation',
        'created_at'
    )


# Register model
admin.site.register(Ticket, TicketAdmin)