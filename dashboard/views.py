from django.shortcuts import render


def home(request):
    context = {
        "project_count": 5,
        "message_count": 2,
        "deadline_count": 3,
    }

    return render(request, "dashboard/home.html", context)