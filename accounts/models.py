from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model.

    Inherits all functionality from Django's AbstractUser
    and adds additional contact information for the student profile.
    """

    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )