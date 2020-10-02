from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail, BadHeaderError 
from django.conf import settings

from problems.models import Problem

from .forms import ProblemForm


def problem_details(request, slug):
    problem = get_object_or_404(Problem, slug=slug)
    context = {"problem": problem}
    return render(request, "problems/details.html", context)


def problem_random(request):
    problem = Problem.objects.random()
    while not problem.published:
        problem = Problem.objects.random()
        
    return redirect(problem)


def problem_select(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id, published=True)
    problem.select()
    request.session["problem_selected"] = problem.id
    return redirect(problem)


def problem_create(request):
    if request.method == "POST":
        form = ProblemForm(request.POST)
        subject = request.POST.get('title')
        author = request.POST.get('author')
        content = request.POST.get('description')
        if form.is_valid() and subject and content:
            problem = form.save()
            problem.author = author
            problem.save()
            send_mail(f'"{subject}" by: "{author}"', content, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)
            return redirect('core:success')
    else:
        form = ProblemForm()
           
    return render(request, 'problems/create.html', {'form': form})


