from django.urls import path
from .views import (
    set_reminder_view,
    reminder_list_view,
    run_scheduler_view
)

urlpatterns = [

    #  Create/Set reminder for a ticket
    path('set/<int:ticket_id>/', set_reminder_view, name='set_reminder'),

    # View all reminders
    path('list/', reminder_list_view, name='reminder_list'),

    #  Run scheduler manually (for demo)
    path('run/', run_scheduler_view, name='run_scheduler'),
]