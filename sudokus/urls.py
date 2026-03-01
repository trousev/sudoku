from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("sudoku/<int:pk>/", views.detail, name="detail"),
    path("generate/", views.generate, name="generate"),
    path("generate/<str:difficulty>/", views.generate_sudoku, name="generate_sudoku"),
    path("sudoku/<int:pk>/delete/", views.delete, name="delete"),
    path("sudoku/<int:pk>/update-status/", views.update_status, name="update_status"),
]
