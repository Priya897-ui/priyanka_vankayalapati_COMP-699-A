from django.urls import path
from .views import predict_ticket_view, compare_tickets_view

urlpatterns = [

    # Main prediction route (core system flow)
    path('predict/<int:ticket_id>/', predict_ticket_view, name='predict_ticket'),

    # Compare two tickets
    path('compare/', compare_tickets_view, name='compare_tickets'),
]