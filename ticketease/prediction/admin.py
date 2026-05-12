from django.contrib import admin
from .models import Prediction


class PredictionAdmin(admin.ModelAdmin):

    # Columns to display
    list_display = (
        'id',
        'ticket',
        'success_probability',
        'risk_index',
        'recommendation',
        'created_at'
    )

    # Filters
    list_filter = (
        'recommendation',
        'created_at'
    )

    # Search capability
    search_fields = (
        'ticket__id',
        'ticket__user__username'
    )

    # Read-only fields (important for integrity)
    readonly_fields = (
        'ticket',
        'success_probability',
        'risk_index',
        'recommendation',
        'explanation',
        'created_at'
    )


# Register model
admin.site.register(Prediction, PredictionAdmin)