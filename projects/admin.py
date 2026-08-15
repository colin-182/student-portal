from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "owner",
        "status",
        "start_date",
        "end_date",
    )

    list_filter = (
        "status",
        "start_date",
        "end_date",
    )

    search_fields = (
        "title",
        "description",
        "owner__username",
    )