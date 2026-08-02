from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProjectForm
from .models import Project


def project_list(request):
    projects = Project.objects.all().order_by("-created_at")

    return render(
        request,
        "projects/project_list.html",
        {
            "projects": projects,
        },
    )


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    return render(
        request,
        "projects/project_detail.html",
        {
            "project": project,
        },
    )

def project_create(request):
    if request.method == "POST":
        form=ProjectForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("projects:list")
        
        else:
            form = ProjectForm()

            return render(
                request,
                "projects/project_form.html",
                {
                    "form": form,
                },
            )