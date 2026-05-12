from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date

from tickets.models import Ticket
from accounts.models import Profile

from .models import Prediction
from .ml_model import get_prediction
from .utils import calculate_risk_index, generate_recommendation


class PredictionLogicTest(TestCase):

    def test_risk_index_calculation(self):
        features = {
            "violation_severity": 3,
            "fine_amount": 500,
            "past_violations": 2,
            "accident_history": 1
        }

        risk = calculate_risk_index(features)

        self.assertIsInstance(risk, float)
        self.assertGreater(risk, 0)

    def test_recommendation_logic(self):
        recommendation = generate_recommendation(0.7, 5)
        self.assertEqual(recommendation, "Contest Ticket")

        recommendation = generate_recommendation(0.2, 12)
        self.assertEqual(recommendation, "Pay Fine")


class MLModelTest(TestCase):

    def test_prediction_output(self):
        features = {
            "violation_severity": 2,
            "fine_amount": 300,
            "past_violations": 1,
            "accident_history": 0
        }

        prob = get_prediction(features)

        self.assertGreaterEqual(prob, 0)
        self.assertLessEqual(prob, 1)


class PredictionViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='preduser',
            password='testpass123'
        )

        self.profile = Profile.objects.create(
            user=self.user,
            past_violations=1,
            accident_history=0
        )

        self.ticket = Ticket.objects.create(
            user=self.user,
            violation_type='speeding',
            location='Hyderabad',
            fine_amount=500,
            ticket_date=date.today()
        )

    def test_prediction_requires_login(self):
        url = f'/prediction/predict/{self.ticket.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_prediction_flow(self):
        self.client.login(username='preduser', password='testpass123')

        url = f'/prediction/predict/{self.ticket.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        # Check prediction created
        prediction = Prediction.objects.filter(ticket=self.ticket).first()
        self.assertIsNotNone(prediction)

        self.assertIsNotNone(prediction.success_probability)
        self.assertIsNotNone(prediction.risk_index)
        self.assertIsNotNone(prediction.recommendation)