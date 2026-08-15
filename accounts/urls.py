from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


app_name = "accounts"


urlpatterns = [

    path(
        "register/",
        views.register,
        name="register",
    ),

    path(
        "profile/",
        views.profile,
        name="profile",
    ),

    path(
        "profile/edit/",
        views.profile_edit,
        name="profile_edit",
    ),

    path(
        "password/change/",
        views.CustomPasswordChangeView.as_view(),
        name="password_change",
    ),

    path(
        "password/change/done/",
        views.password_change_done,
        name="password_change_done",
    ),

    path(
        "password/reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset.html",
            email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
            success_url="/accounts/password/reset/done/",
        ),
        name="password_reset",
    ),

    path(
        "password/reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html",
        ),
        name="password_reset_done",
    ),

    path(
        "password/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url="/accounts/password/reset/complete/",
        ),
        name="password_reset_confirm",
    ),

    path(
        "password/reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]