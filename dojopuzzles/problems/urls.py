from django.urls import path

from problems import views


app_name = "problems"

urlpatterns = [
    path("random/", views.problem_random, name="problem_random"),
    path("select/<int:problem_id>", views.problem_select, name="problem_select"),
    path("<slug:slug>/", views.problem_details, name="problem_details"),
]
