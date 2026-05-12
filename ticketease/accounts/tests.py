from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile


class UserProfileTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_user_created(self):
        self.assertEqual(self.user.username, 'testuser')

    def test_profile_created(self):
        profile = Profile.objects.get(user=self.user)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.past_violations, 0)
        self.assertEqual(profile.accident_history, 0)


class LoginTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='loginuser',
            password='loginpass123'
        )

    def test_login_success(self):
        login = self.client.login(
            username='loginuser',
            password='loginpass123'
        )
        self.assertTrue(login)

    def test_login_fail(self):
        login = self.client.login(
            username='loginuser',
            password='wrongpass'
        )
        self.assertFalse(login)