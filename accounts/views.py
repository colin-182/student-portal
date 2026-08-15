from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import ProfileForm, RegisterForm


def register(request):

    if request.user.is_authenticated:
        return redirect("dashboard:home")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Your account has been created successfully.",
            )

            return redirect(
                "dashboard:home",
            )

    else:

        form = RegisterForm()

    return render(
        request,
        "registration/register.html",
        {
            "form": form,
        },
    )


@login_required
def profile(request):

    return render(
        request,
        "registration/profile.html",
        {
            "profile_user": request.user,
        },
    )


@login_required
def profile_edit(request):

    if request.method == "POST":

        form = ProfileForm(
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
                "accounts:profile",
            )

    else:

        form = ProfileForm(
            instance=request.user,
        )

    return render(
        request,
        "registration/profile_edit.html",
        {
            "form": form,
        },
    )


class CustomPasswordChangeView(PasswordChangeView):

    template_name = "registration/password_change.html"

    success_url = reverse_lazy(
        "accounts:password_change_done",
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Your password has been changed successfully.",
        )

        return super().form_valid(form)


@login_required
def password_change_done(request):

    return render(
        request,
        "registration/password_change_done.html",
    )