from django.contrib import admin
from .models import Sudoku


@admin.register(Sudoku)
class SudokuAdmin(admin.ModelAdmin):
    list_display = ["name", "difficulty", "created_at", "updated_at"]
    list_filter = ["difficulty"]
    search_fields = ["name"]
