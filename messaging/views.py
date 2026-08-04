from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MessageForm
from .models import Message


@login_required
def inbox(request):
    messages = (
        Message.objects.filter(recipient=request.user)
        .order_by("-sent_at")
    )

    return render(
        request,
        "messaging/inbox.html",
        {
            "messages": messages,
        },
    )


@login_required
def message_detail(request, pk):
    message = get_object_or_404(
        Message,
        pk=pk,
        recipient=request.user,
    )

    return render(
        request,
        "messaging/message_detail.html",
        {
            "message": message,
        },
    )


@login_required
def message_create(request):
    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()

            return redirect("messaging:inbox")

    else:
        form = MessageForm()

    return render(
        request,
        "messaging/message_form.html",
        {
            "form": form,
        },
    )