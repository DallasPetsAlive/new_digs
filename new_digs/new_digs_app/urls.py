from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("participant_app/", views.participant_app, name="participant_app"),
]
