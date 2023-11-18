from django.urls import path

from . import views

urlpatterns = [
    path("siRNA", views.run_sirna_off_target_search, name="Run siRNA Off Target Search"),
    path("ASO", views.run_aso_off_target_search, name="Run ASO Off Target Search"),
    path("Check", views.run_check_file, name="Run Check file existence"),
]
