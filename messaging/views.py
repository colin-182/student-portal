from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MessageForm
from .models import Message


@login_required
def inbox(request):
    """Display the current user's active received messages."""
    inbox_messages = Message.objects.filter(
        recipient=request.user,
        is_archived=False,
    )

    return render(
        request,
        "messaging/inbox.html",
        {
            "inbox_messages": inbox_messages,
        },
    )


@login_required
def sent_messages(request):
    """Display messages sent by the current user."""
    sent_messages = Message.objects.filter(
        sender=request.user,
    )

    return render(
        request,
        "messaging/sent_messages.html",
        {
            "sent_messages": sent_messages,
        },
    )


@login_required
def archived_messages(request):
    """Display archived messages received by the current user."""
    archived_messages = Message.objects.filter(
        recipient=request.user,
        is_archived=True,
    )

    return render(
        request,
        "messaging/archived_messages.html",
        {
            "archived_messages": archived_messages,
        },
    )


@login_required
def message_detail(request, pk):
    """Display a message accessible to the current user."""
    message = get_object_or_404(
        Message.objects.filter(
            Q(recipient=request.user) | Q(sender=request.user),
        ),
        pk=pk,
    )

    is_sender = message.sender == request.user

    # Opening a received message marks it as read.
    if not is_sender and not message.is_read:
        message.is_read = True
        message.save(update_fields=["is_read"])

    return render(
        request,
        "messaging/message_detail.html",
        {
            "message": message,
            "is_sender": is_sender,
        },
    )


@login_required
def message_create(request):
    """Create and send a new message from the current user."""
    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()

            messages.success(
                request,
                "Message sent successfully.",
            )

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


@login_required
def message_reply(request, pk):
    """Reply to a message received by the current user."""
    original_message = get_object_or_404(
        Message,
        pk=pk,
        recipient=request.user,
    )

    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            reply = form.save(commit=False)

            # Set these fields server-side so they cannot be
            # changed through submitted form data.
            reply.sender = request.user
            reply.recipient = original_message.sender
            reply.save()

            messages.success(
                request,
                "Reply sent successfully.",
            )

            return redirect("messaging:sent")

    else:
        form = MessageForm(
            initial={
                "recipient": original_message.sender,
                "subject": f"Re: {original_message.subject}",
            }
        )

    return render(
        request,
        "messaging/message_form.html",
        {
            "form": form,
        },
    )


@login_required
def archive_message(request, pk):
    """Archive a message received by the current user."""
    message = get_object_or_404(
        Message,
        pk=pk,
        recipient=request.user,
    )

    if request.method == "POST":
        message.is_archived = True
        message.save(update_fields=["is_archived"])

        messages.success(
            request,
            "Message archived successfully.",
        )

        return redirect("messaging:inbox")

    return redirect(
        "messaging:detail",
        pk=message.pk,
    )


@login_required
def restore_message(request, pk):
    """Restore an archived message for the current user."""
    message = get_object_or_404(
        Message,
        pk=pk,
        recipient=request.user,
    )

    if request.method == "POST":
        message.is_archived = False
        message.save(update_fields=["is_archived"])

        messages.success(
            request,
            "Message restored successfully.",
        )

        return redirect("messaging:archived")

    return redirect(
        "messaging:detail",
        pk=message.pk,
    )


@login_required
def message_delete(request, pk):
    """Permanently delete a message received by the current user."""
    message = get_object_or_404(
        Message,
        pk=pk,
        recipient=request.user,
    )

    if request.method == "POST":
        message.delete()

        messages.success(
            request,
            "Message deleted successfully.",
        )

        return redirect("messaging:inbox")

    return render(
        request,
        "messaging/message_confirm_delete.html",
        {
            "message": message,
        },
    )