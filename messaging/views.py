from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import MessageForm


@login_required
def message_create(request):
    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()

            return redirect("dashboard:home")

    else:
        form = MessageForm()

    return render(
        request,
        "messaging/message_form.html",
        {
            "form": form,
        },
    )