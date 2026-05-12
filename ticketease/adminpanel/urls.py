from django.urls import path
from .views import (
    admin_dashboard_view,
    ocr_logs_view,
    ml_logs_view,
    report_view
)

urlpatterns = [

    # Admin Dashboard
    path('dashboard/', admin_dashboard_view, name='admin_dashboard'),

    # OCR Logs (simulated)
    path('ocr-logs/', ocr_logs_view, name='ocr_logs'),

    # ML Logs
    path('ml-logs/', ml_logs_view, name='ml_logs'),

    # Reports
    path('reports/', report_view, name='admin_reports'),
]