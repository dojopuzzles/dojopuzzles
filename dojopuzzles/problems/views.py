from django.shortcuts import render
from django.shortcuts import get_object_or_404

from problems.models import Problem


def problem_details(request, slug):
    problem = get_object_or_404(Problem, slug=slug)
    context = {"problem": problem}
    return render(request, "problems/details.html", context)


def problem_random(request):
    problem = Problem.objects.random()

    # TODO redirect instead of render
    context = {"problem": problem}
    return render(request, "problems/details.html", context)
