from django.urls import path

from . import views

app_name = "messaging"

urlpatterns = [
    path(
        "new/",
        views.message_create,
        name="create",
    ),
]