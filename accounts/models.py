from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom user model.

    Inherits all functionality from Django's AbstractUser.
    Extra fields can be added here later.
    """

    pass