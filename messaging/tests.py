from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Message


User = get_user_model()


class MessageModelTests(TestCase):
    """Tests for message model behaviour."""

    def setUp(self):
        self.sender = User.objects.create_user(
            username="sender",
            password="TestPassword123!",
        )

        self.recipient = User.objects.create_user(
            username="recipient",
            password="TestPassword123!",
        )

    def test_message_string_representation(self):
        """The message string representation is its subject."""
        message = Message.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            subject="Test Subject",
            body="Test message body.",
        )

        self.assertEqual(str(message), "Test Subject")


class MessageViewTests(TestCase):
    """Tests for messaging access and behaviour."""

    def setUp(self):
        self.sender = User.objects.create_user(
            username="sender",
            password="TestPassword123!",
        )

        self.recipient = User.objects.create_user(
            username="recipient",
            password="TestPassword123!",
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="TestPassword123!",
        )

        self.message = Message.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            subject="Test Subject",
            body="Test message body.",
        )

    def test_inbox_requires_login(self):
        """Unauthenticated users are redirected to login."""
        response = self.client.get("/messaging/")

        self.assertEqual(response.status_code, 302)

    def test_recipient_can_view_inbox(self):
        """A recipient can view their inbox."""
        self.client.login(
            username="recipient",
            password="TestPassword123!",
        )

        response = self.client.get("/messaging/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Subject")

    def test_sender_can_view_sent_messages(self):
        """A sender can view messages they have sent."""
        self.client.login(
            username="sender",
            password="TestPassword123!",
        )

        response = self.client.get("/messaging/sent/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Subject")

    def test_opening_received_message_marks_it_as_read(self):
        """Opening an unread received message marks it as read."""
        self.client.login(
            username="recipient",
            password="TestPassword123!",
        )

        self.assertFalse(self.message.is_read)

        response = self.client.get(
            f"/messaging/{self.message.pk}/",
        )

        self.assertEqual(response.status_code, 200)

        self.message.refresh_from_db()

        self.assertTrue(self.message.is_read)

    def test_other_user_cannot_view_message(self):
        """Users cannot view messages they did not send or receive."""
        self.client.login(
            username="otheruser",
            password="TestPassword123!",
        )

        response = self.client.get(
            f"/messaging/{self.message.pk}/",
        )

        self.assertEqual(response.status_code, 404)

    def test_recipient_can_archive_message(self):
        """A recipient can archive a message."""
        self.client.login(
            username="recipient",
            password="TestPassword123!",
        )

        response = self.client.post(
            f"/messaging/{self.message.pk}/archive/",
        )

        self.assertEqual(response.status_code, 302)

        self.message.refresh_from_db()

        self.assertTrue(self.message.is_archived)

    def test_recipient_can_restore_message(self):
        """A recipient can restore an archived message."""
        self.message.is_archived = True
        self.message.save(update_fields=["is_archived"])

        self.client.login(
            username="recipient",
            password="TestPassword123!",
        )

        response = self.client.post(
            f"/messaging/{self.message.pk}/restore/",
        )

        self.assertEqual(response.status_code, 302)

        self.message.refresh_from_db()

        self.assertFalse(self.message.is_archived)

    def test_recipient_can_delete_message(self):
        """A recipient can permanently delete a message."""
        self.client.login(
            username="recipient",
            password="TestPassword123!",
        )

        response = self.client.post(
            f"/messaging/{self.message.pk}/delete/",
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Message.objects.filter(
                pk=self.message.pk,
            ).exists()
        )

    def test_sender_cannot_archive_received_message(self):
        """Only the recipient can archive a message."""
        self.client.login(
            username="sender",
            password="TestPassword123!",
        )

        response = self.client.post(
            f"/messaging/{self.message.pk}/archive/",
        )

        self.assertEqual(response.status_code, 404)

        self.message.refresh_from_db()

        self.assertFalse(self.message.is_archived)