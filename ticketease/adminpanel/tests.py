from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AdminPanelViewTest(TestCase):

    def setUp(self):
        # Create normal user
        self.user = User.objects.create_user(
            username='normaluser',
            password='testpass123'
        )

        # Create admin (staff) user
        self.admin_user = User.objects.create_user(
            username='adminuser',
            password='adminpass123',
            is_staff=True
        )

    # -----------------------------
    # Access Control Tests
    # -----------------------------
    def test_dashboard_requires_admin(self):
        response = self.client.get('/adminpanel/dashboard/')
        self.assertEqual(response.status_code, 302)  # redirect

    def test_dashboard_admin_access(self):
        self.client.login(username='adminuser', password='adminpass123')
        response = self.client.get('/adminpanel/dashboard/')
        self.assertEqual(response.status_code, 200)

    # -----------------------------
    # OCR Logs View
    # -----------------------------
    def test_ocr_logs_access(self):
        self.client.login(username='adminuser', password='adminpass123')
        response = self.client.get('/adminpanel/ocr-logs/')
        self.assertEqual(response.status_code, 200)

    # -----------------------------
    # ML Logs View
    # -----------------------------
    def test_ml_logs_access(self):
        self.client.login(username='adminuser', password='adminpass123')
        response = self.client.get('/adminpanel/ml-logs/')
        self.assertEqual(response.status_code, 200)

    # -----------------------------
    # Reports View
    # -----------------------------
    def test_reports_access(self):
        self.client.login(username='adminuser', password='adminpass123')
        response = self.client.get('/adminpanel/reports/')
        self.assertEqual(response.status_code, 200)