from django.shortcuts import render

from problems.models import Problem


def home(request):
    most_used = Problem.objects.most_used()[:5]
    problems_used = Problem.objects.total_used()
    return render(
        request,
        "core/home.html",
        context={"problems_used": problems_used, "most_used": most_used},
    )


def about(request):
    return render(request, "core/about.html")


def success(request):
    return render(request, 'core/success.html')
