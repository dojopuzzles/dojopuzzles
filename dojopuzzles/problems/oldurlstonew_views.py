# views to redirect old urls format to new ones.
from django.shortcuts import redirect


def problem_details_redirect(request, slug):
    return redirect("problems:problem_details", slug=slug)


def problem_random_redirect(request):
    return redirect("problems:problem_random")


def problem_select_redirect(request, problem_id):
    return redirect("problems:problem_select", problem_id=problem_id)
