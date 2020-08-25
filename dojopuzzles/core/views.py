from django.shortcuts import render

from problems.models import Problem


def home(request):
    most_used = Problem.objects.most_used()[:5]
    return render(request, "core/home.html", context={"most_used": most_used})


def about(request):
    return render(request, "core/about.html")
