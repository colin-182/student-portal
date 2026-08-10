from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from messaging.models import Message
from projects.models import Project

from .forms import ProfileUpdateForm


@login_required
def home(request):

    project_count = Project.objects.filter(
        owner=request.user,
    ).count()

    unread_messages = Message.objects.filter(
        recipient=request.user,
        is_read=False,
    ).count()

    total_messages = Message.objects.filter(
        recipient=request.user,
    ).count()

    recent_projects = Project.objects.filter(
        owner=request.user,
    ).order_by("-created_at")[:5]

    recent_messages = Message.objects.filter(
        recipient=request.user,
    ).order_by("-sent_at")[:5]

    context = {
        "project_count": project_count,
        "unread_messages": unread_messages,
        "total_messages": total_messages,
        "recent_projects": recent_projects,
        "recent_messages": recent_messages,
    }

    return render(
        request,
        "dashboard/home.html",
        context,
    )


@login_required
def profile(request):

    context = {
        "project_count": Project.objects.filter(
            owner=request.user,
        ).count(),

        "messages_sent": Message.objects.filter(
            sender=request.user,
        ).count(),

        "messages_received": Message.objects.filter(
            recipient=request.user,
        ).count(),

        "unread_messages": Message.objects.filter(
            recipient=request.user,
            is_read=False,
        ).count(),
    }

    return render(
        request,
        "dashboard/profile.html",
        context,
    )


@login_required
def profile_edit(request):

    if request.method == "POST":

        form = ProfileUpdateForm(
            request.POST,
            instance=request.user,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Your profile has been updated successfully.",
            )

            return redirect(
                "dashboard:profile",
            )

    else:

        form = ProfileUpdateForm(
            instance=request.user,
        )

    return render(
        request,
        "dashboard/profile_edit.html",
        {
            "form": form,
        },
    )