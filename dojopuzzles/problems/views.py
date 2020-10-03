from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, redirect, render

from problems.models import Problem


def problem_details(request, slug):
    problem = get_object_or_404(Problem, slug=slug)
    context = {"problem": problem}
    return render(request, "problems/details.html", context)


def problem_random(request):
    problem = Problem.objects.random()

    return redirect(problem)


def problem_select(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id, published=True)
    problem.select()
    request.session["problem_selected"] = problem.id
    return redirect(problem)


def problem_list(request):
    problems = Problem.objects.published()
    page = request.GET.get('page')
    paginator = Paginator(problems, 15)

    try:
        problems = paginator.page(page)
    except PageNotAnInteger:
        problems = paginator.page(1)
    except EmptyPage:
        problems = paginator.page(paginator.num_pages)

    return render(request, "problems/list.html", {"problems": problems})
