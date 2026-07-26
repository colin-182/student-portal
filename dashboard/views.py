from django.shortcuts import render


def home(request):
    return render(request, "dashboard/home.html")


def projects(request):
    return render(request, "dashboard/projects.html")


def messages(request):
    return render(request, "dashboard/messages.html")


def profile(request):
    return render(request, "dashboard/profile.html")