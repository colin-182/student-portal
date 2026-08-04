from django.urls import path
from . import views

app_name = "messaging"

print("=== LOADING MESSAGING URLS ===")

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("sent/", views.sent_messages, name="sent"),
    path("new/", views.message_create, name="new"),
    path("<int:pk>/", views.message_detail, name="detail"),
]