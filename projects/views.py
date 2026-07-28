from django.shortcuts import render
from .models import Project


def project_list(request):
    print("APP:", request.resolver_match.app_name)
    print("URL:", request.resolver_match.url_name)

    projects = Project.objects.all().order_by("-created_at")

    return render(
        request,
        "projects/project_list.html",
        {
            "projects": projects,
        },
    )