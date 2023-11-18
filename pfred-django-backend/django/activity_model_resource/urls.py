from django.urls import path

from . import views

urlpatterns = [
    path("siRNA", views.run_sirna_activity_model, name="Run siRNA Activity Model"),
    path("ASO", views.run_aso_activity_model, name="Run ASO Activity Model"),
]
