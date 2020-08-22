from django.urls import path

from problems import views


app_name = "problems"

urlpatterns = [
    path("random/", views.problem_random, name="problem_random"),
    path("<slug:slug>/", views.problem_details, name="problem_details"),
]
