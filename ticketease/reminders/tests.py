from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, timedelta

from tickets.models import Ticket
from .models import Reminder
from .scheduler import process_due_reminders


class ReminderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='reminderuser',
            password='testpass123'
        )

        self.ticket = Ticket.objects.create(
            user=self.user,
            violation_type='parking',
            location='Hyderabad',
            fine_amount=300,
            ticket_date=date.today()
        )

    def test_reminder_creation(self):
        reminder = Reminder.objects.create(
            user=self.user,
            ticket=self.ticket,
            reminder_date=date.today()
        )

        self.assertEqual(reminder.user.username, 'reminderuser')
        self.assertFalse(reminder.is_sent)


class SchedulerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='scheduleruser',
            password='testpass123'
        )

        self.ticket = Ticket.objects.create(
            user=self.user,
            violation_type='speeding',
            location='Delhi',
            fine_amount=500,
            ticket_date=date.today()
        )

    def test_scheduler_process_due(self):
        # Create a due reminder
        Reminder.objects.create(
            user=self.user,
            ticket=self.ticket,
            reminder_date=date.today()
        )

        count = process_due_reminders()

        reminder = Reminder.objects.first()

        self.assertEqual(count, 1)
        self.assertTrue(reminder.is_sent)

    def test_scheduler_future_reminder(self):
        # Future reminder should not be processed
        Reminder.objects.create(
            user=self.user,
            ticket=self.ticket,
            reminder_date=date.today() + timedelta(days=5)
        )

        count = process_due_reminders()

        reminder = Reminder.objects.first()

        self.assertEqual(count, 0)
        self.assertFalse(reminder.is_sent)


class ReminderViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='viewuser',
            password='testpass123'
        )

        self.ticket = Ticket.objects.create(
            user=self.user,
            violation_type='signal violation',
            location='Mumbai',
            fine_amount=700,
            ticket_date=date.today()
        )

    def test_set_reminder_requires_login(self):
        response = self.client.get(f'/reminders/set/{self.ticket.id}/')
        self.assertEqual(response.status_code, 302)

    def test_set_reminder(self):
        self.client.login(username='viewuser', password='testpass123')

        response = self.client.post(f'/reminders/set/{self.ticket.id}/', {
            'reminder_date': str(date.today()),
            'message': 'Pay before due'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reminder.objects.count(), 1)

    def test_reminder_list_view(self):
        self.client.login(username='viewuser', password='testpass123')

        Reminder.objects.create(
            user=self.user,
            ticket=self.ticket,
            reminder_date=date.today()
        )

        response = self.client.get('/reminders/list/')
        self.assertEqual(response.status_code, 200)

    def test_run_scheduler_view(self):
        self.client.login(username='viewuser', password='testpass123')

        Reminder.objects.create(
            user=self.user,
            ticket=self.ticket,
            reminder_date=date.today()
        )

        response = self.client.get('/reminders/run/')
        self.assertEqual(response.status_code, 302)