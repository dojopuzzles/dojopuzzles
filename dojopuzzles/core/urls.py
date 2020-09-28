from django.urls import path

from core import views


app_name = "core"

urlpatterns = [
    path("home/", views.home, name="home"),
    path("about/", views.about, name="about"),
]
