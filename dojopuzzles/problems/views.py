from django.shortcuts import get_object_or_404, redirect, render

from problems.models import Problem


def problem_details(request, slug):
    problem = get_object_or_404(Problem, slug=slug)
    context = {"problem": problem}
    return render(request, "problems/details.html", context)


def problem_random(request):
    problem = Problem.objects.random()

    return redirect(problem)
