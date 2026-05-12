from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date

from .models import Ticket
from .services import extract_ticket_data, clean_text


class TicketModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='ticketuser',
            password='testpass123'
        )

    def test_ticket_creation(self):
        ticket = Ticket.objects.create(
            user=self.user,
            violation_type='speeding',
            location='Hyderabad',
            fine_amount=500,
            ticket_date=date.today()
        )

        self.assertEqual(ticket.user.username, 'ticketuser')
        self.assertEqual(ticket.violation_type, 'speeding')
        self.assertTrue(ticket.is_saved)


class ServiceTest(TestCase):

    def test_extract_ticket_data(self):
        form_data = {
            'violation_type': 'speeding',
            'location': 'Hyderabad',
            'fine_amount': '500',
            'ticket_date': '2024-01-01'
        }

        result = extract_ticket_data(form_data)

        self.assertEqual(result['violation_type'], 'speeding')
        self.assertEqual(result['location'], 'Hyderabad')
        self.assertEqual(result['fine_amount'], 500.0)
        self.assertIn('Violation:', result['extracted_text'])

    def test_clean_text(self):
        raw_text = "Violation: SPEEDING!!   Location: Hyderabad@@"
        cleaned = clean_text(raw_text)

        self.assertNotIn('!!', cleaned)
        self.assertEqual(cleaned, cleaned.lower())


class TicketViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='viewuser',
            password='testpass123'
        )

    def test_upload_requires_login(self):
        response = self.client.get('/tickets/upload/')
        self.assertEqual(response.status_code, 302)  # redirect to login

    def test_upload_ticket(self):
        self.client.login(username='viewuser', password='testpass123')

        response = self.client.post('/tickets/upload/', {
            'violation_type': 'parking',
            'location': 'Mumbai',
            'fine_amount': '300',
            'ticket_date': '2024-01-01'
        })

        # Should redirect to prediction page
        self.assertEqual(response.status_code, 302)

        # Ticket should be created
        self.assertEqual(Ticket.objects.count(), 1)

    def test_ticket_list_view(self):
        self.client.login(username='viewuser', password='testpass123')

        Ticket.objects.create(
            user=self.user,
            violation_type='parking',
            location='Delhi',
            fine_amount=200,
            ticket_date=date.today()
        )

        response = self.client.get('/tickets/cases/')
        self.assertEqual(response.status_code, 200)