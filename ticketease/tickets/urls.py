from django.urls import path
from .views import (
    upload_ticket_view,
    ticket_detail_view,
    ticket_list_view,
    delete_ticket_view,
    edit_ticket_view
)

urlpatterns = [

    # Enter / Upload Ticket
    path('upload/', upload_ticket_view, name='upload_ticket'),

    # View all saved tickets
    path('cases/', ticket_list_view, name='ticket_list'),

    # View single ticket result
    path('detail/<int:ticket_id>/', ticket_detail_view, name='ticket_detail'),

    # Edit ticket
    path('edit/<int:ticket_id>/', edit_ticket_view, name='edit_ticket'),

    # Delete ticket
    path('delete/<int:ticket_id>/', delete_ticket_view, name='delete_ticket'),
]