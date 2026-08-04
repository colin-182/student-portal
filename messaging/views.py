from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MessageForm
from .models import Message


@login_required
def inbox(request):
    messages = Message.objects.filter(
        recipient=request.user,
    )

    return render(
        request,
        "messaging/inbox.html",
        {
            "messages": messages,
        },
    )


@login_required
def sent_messages(request):
    messages = Message.objects.filter(
        sender=request.user,
    )

    return render(
        request,
        "messaging/sent_messages.html",
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

    if not message.is_read:
        message.is_read = True
        message.save()

    return render(
        request,
        "messaging/message_detail.html",
        {
            "message": message,
        },
    )


@login_required
def message_create(request):
    initial = {}

    recipient_id = request.GET.get("recipient")
    subject = request.GET.get("subject")

    if recipient_id:
        initial["recipient"] = recipient_id

    if subject:
        initial["subject"] = subject

    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()

            return redirect("messaging:inbox")

    else:
        form = MessageForm(initial=initial)

    return render(
        request,
        "messaging/message_form.html",
        {
            "form": form,
        },
    )