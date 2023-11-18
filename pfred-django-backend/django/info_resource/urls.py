from django.urls import path

from . import views

urlpatterns = [
    path("Version", views.get_version, name="Fetch service version"),
]
