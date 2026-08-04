from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from messaging.models import Message
from projects.models import Project


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