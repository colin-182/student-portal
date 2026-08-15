from django.contrib.auth import get_user_model
from django.test import TestCase

from .forms import ProfileForm, RegisterForm


User = get_user_model()


class RegistrationFormTests(TestCase):
    """Tests for user registration."""

    def test_valid_registration_form(self):
        """A valid registration form is accepted."""
        form = RegisterForm(
            data={
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "TestPassword123!",
                "password2": "TestPassword123!",
            }
        )

        self.assertTrue(form.is_valid())

    def test_duplicate_username_is_rejected(self):
        """A username already in use cannot be registered again."""
        User.objects.create_user(
            username="existinguser",
            password="TestPassword123!",
        )

        form = RegisterForm(
            data={
                "username": "existinguser",
                "email": "newuser@example.com",
                "password1": "TestPassword123!",
                "password2": "TestPassword123!",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


class ProfileFormTests(TestCase):
    """Tests for profile form validation."""

    def test_profile_form_accepts_valid_data(self):
        """A valid profile form is accepted."""
        user = User.objects.create_user(
            username="profileuser",
            password="TestPassword123!",
        )

        form = ProfileForm(
            data={
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com",
                "phone_number": "0123456789",
                "address": "Test Address",
            },
            instance=user,
        )

        self.assertTrue(form.is_valid())


class AccountViewTests(TestCase):
    """Tests for account authentication and profile access."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123!",
        )

    def test_profile_requires_login(self):
        """Unauthenticated users cannot access the profile."""
        response = self.client.get("/accounts/profile/")

        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_view_profile(self):
        """An authenticated user can access their profile."""
        self.client.login(
            username="testuser",
            password="TestPassword123!",
        )

        response = self.client.get("/accounts/profile/")

        self.assertEqual(response.status_code, 200)