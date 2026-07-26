from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("projects/", views.projects, name="projects"),
    path("messages/", views.messages, name="messages"),
    path("profile/", views.profile, name="profile"),
]