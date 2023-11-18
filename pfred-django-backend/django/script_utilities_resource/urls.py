from django.urls import path

from . import views

urlpatterns = [
    path("Orthologs", views.get_orthologs, name="Run get Orthologs"),
    path("enumerate_first", views.enumerate_first, name="Run enumerate"),
    # was "Run enumerate" in original code, worried about name conflicts
    path("enumerate_second", views.enumerate_second, name="Run enumerate 2"),
    path("clean", views.clean_run_dir, name="Run clean run directory"),
    # was "Run clean run directory" in original code, worried about name conflicts
    path("appendToFile", views.append_to_file, name="Run append to file"),
]
