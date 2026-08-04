from django.urls import path

from . import views

app_name = "messaging"

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("new/", views.message_create, name="new"),
    path("<int:pk>/", views.message_detail, name="detail"),
]