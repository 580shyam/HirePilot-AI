from django.urls import path
from analyzer import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/health/", views.health, name="health"),
    path("api/analyze/", views.analyze, name="analyze"),
]
