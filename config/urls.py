from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("dashboard.urls")),

    path("projects/", include("projects.urls")),

    # We'll add these later
    # path("messages/", include("messaging.urls")),
    # path("accounts/", include("accounts.urls")),
]