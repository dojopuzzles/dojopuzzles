# handles the old routes and match them to views that redirects to new urls format
from django.urls import path

from problems import oldurlstonew_views as views

urlpatterns = [
    path("exibe/random/", views.problem_random_redirect),
    path(
        "exibe/select/<int:problem_id>",
        views.problem_select_redirect,
    ),
    path("exibe/<slug:slug>/", views.problem_details_redirect),
]
