from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from .forms import ProjectForm
from .models import Project


User = get_user_model()


class ProjectModelTests(TestCase):
    """Tests for project model behaviour."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="projectuser",
            password="TestPassword123!",
        )

    def test_project_string_representation(self):
        """The project's string representation is its title."""
        project = Project.objects.create(
            owner=self.user,
            title="Test Project",
        )

        self.assertEqual(str(project), "Test Project")

    def test_end_date_cannot_be_before_start_date(self):
        """Projects reject an end date earlier than their start date."""
        project = Project(
            owner=self.user,
            title="Invalid Project",
            start_date=date(2026, 8, 20),
            end_date=date(2026, 8, 10),
        )

        form = ProjectForm(
            data={
                "title": project.title,
                "description": "",
                "start_date": project.start_date,
                "end_date": project.end_date,
                "stakeholders": "",
                "status": Project.Status.PLANNING,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("end_date", form.errors)

    def test_project_can_be_created(self):
        """A valid project can be created successfully."""
        project = Project.objects.create(
            owner=self.user,
            title="Valid Project",
            description="A test project.",
            status=Project.Status.ACTIVE,
        )

        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(project.owner, self.user)
        self.assertEqual(project.status, Project.Status.ACTIVE)


class ProjectViewTests(TestCase):
    """Tests for project access and ownership."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="projectowner",
            password="TestPassword123!",
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="TestPassword123!",
        )

        self.project = Project.objects.create(
            owner=self.user,
            title="My Project",
        )

    def test_project_list_requires_login(self):
        """Unauthenticated users are redirected to login."""
        response = self.client.get("/projects/")

        self.assertEqual(response.status_code, 302)

    def test_project_list_shows_owned_projects(self):
        """Authenticated users can view their own projects."""
        self.client.login(
            username="projectowner",
            password="TestPassword123!",
        )

        response = self.client.get("/projects/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My Project")

    def test_project_detail_is_restricted_to_owner(self):
        """Users cannot access another user's project."""
        self.client.login(
            username="otheruser",
            password="TestPassword123!",
        )

        response = self.client.get(
            f"/projects/{self.project.pk}/",
        )

        self.assertEqual(response.status_code, 404)