from django.urls import path

from . import views

app_name = "messaging"

urlpatterns = [
    path(
        "",
        views.inbox,
        name="inbox",
    ),

    path(
        "sent/",
        views.sent_messages,
        name="sent",
    ),

    path(
        "archived/",
        views.archived_messages,
        name="archived",
    ),

    path(
        "new/",
        views.message_create,
        name="new",
    ),

    path(
        "<int:pk>/",
        views.message_detail,
        name="detail",
    ),

    path(
        "<int:pk>/reply/",
        views.message_reply,
        name="reply",
    ),

    path(
        "<int:pk>/archive/",
        views.archive_message,
        name="archive",
    ),

    path(
        "<int:pk>/restore/",
        views.restore_message,
        name="restore",
    ),

    path(
        "<int:pk>/delete/",
        views.message_delete,
        name="delete",
    ),
]