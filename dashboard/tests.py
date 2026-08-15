from django.contrib.auth import get_user_model
from django.test import TestCase

from messaging.models import Message
from projects.models import Project


User = get_user_model()


class DashboardViewTests(TestCase):
    """Tests for dashboard access and displayed information."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="dashboarduser",
            password="TestPassword123!",
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="TestPassword123!",
        )

    def test_dashboard_requires_login(self):
        """Unauthenticated users are redirected to login."""
        response = self.client.get("/")

        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_view_dashboard(self):
        """Authenticated users can access the dashboard."""
        self.client.login(
            username="dashboarduser",
            password="TestPassword123!",
        )

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

    def test_dashboard_displays_project_count(self):
        """The dashboard displays the user's project count."""
        Project.objects.create(
            owner=self.user,
            title="Dashboard Project",
        )

        self.client.login(
            username="dashboarduser",
            password="TestPassword123!",
        )

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["project_count"], 1)

    def test_dashboard_displays_message_counts(self):
        """The dashboard displays received and unread message counts."""
        Message.objects.create(
            sender=self.other_user,
            recipient=self.user,
            subject="Dashboard Message",
            body="Test message.",
        )

        self.client.login(
            username="dashboarduser",
            password="TestPassword123!",
        )

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_messages"], 1)
        self.assertEqual(response.context["unread_messages"], 1)

    def test_dashboard_only_counts_users_own_projects(self):
        """The dashboard excludes projects belonging to other users."""
        Project.objects.create(
            owner=self.user,
            title="My Project",
        )

        Project.objects.create(
            owner=self.other_user,
            title="Other Project",
        )

        self.client.login(
            username="dashboarduser",
            password="TestPassword123!",
        )

        response = self.client.get("/")

        self.assertEqual(response.context["project_count"], 1)