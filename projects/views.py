from django.contrib.auth.decorators import login_required
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


@login_required
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()

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


@login_required
def project_update(request, pk):
    project = get_object_or_404(
        Project,
        pk=pk,
    )

    if request.method == "POST":
        form = ProjectForm(
            request.POST,
            instance=project,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "projects:detail",
                pk=project.pk,
            )

    else:
        form = ProjectForm(
            instance=project,
        )

    return render(
        request,
        "projects/project_form.html",
        {
            "form": form,
        },
    )

@login_required
def project_delete(request, pk):
    project = get_object_or_404(
        Project,
        pk=pk,
    )

    if request.method == "POST":
        project.delete()

        return redirect(
            "projects:list",
        )

    return render(
        request,
        "projects/project_confirm_delete.html",
        {
            "project": project,
        },
    )