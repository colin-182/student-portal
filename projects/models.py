from django.conf import settings
from django.db import models


class Project(models.Model):

    class Status(models.TextChoices):
        PLANNING = "PL", "Planning"
        ACTIVE = "AC", "Active"
        COMPLETED = "CO", "Completed"

    title = models.CharField(max_length=200)

    description = models.TextField(
        blank=True
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
    )

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PLANNING,
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    stakeholders = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title