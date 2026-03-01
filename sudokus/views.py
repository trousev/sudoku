from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import Sudoku


def home(request):
    difficulty_filter = request.GET.get("difficulty")
    if difficulty_filter:
        sudokus = Sudoku.objects.filter(difficulty=difficulty_filter)
    else:
        sudokus = Sudoku.objects.all()
    return render(request, "sudokus/home.html", {"sudokus": sudokus})


def detail(request, pk):
    sudoku = get_object_or_404(Sudoku, pk=pk)
    return render(request, "sudokus/detail.html", {"sudoku": sudoku})


def generate(request):
    if request.method == "POST":
        difficulty = request.POST.get("difficulty", "Easy")
        return redirect("generate_sudoku", difficulty=difficulty)
    difficulties = ["Easy", "Medium", "Hard", "Extreme"]
    return render(request, "sudokus/generate.html", {"difficulties": difficulties})


def delete(request, pk):
    sudoku = get_object_or_404(Sudoku, pk=pk)
    if request.method == "POST":
        sudoku.delete()
        return redirect("home")
    return render(request, "sudokus/delete.html", {"sudoku": sudoku})


DIFFICULTY_TO_EMPTY = {
    "Easy": 30,
    "Medium": 40,
    "Hard": 50,
    "Extreme": 55,
}


def generate_sudoku(request, difficulty):
    from sudoku import Sudoku as SudokuGenerator
    
    empty_blocks = DIFFICULTY_TO_EMPTY.get(difficulty, 30)
    generator = SudokuGenerator(3, 3)
    puzzle_grid = generator.board
    puzzle = Sudoku(3, 3, board=puzzle_grid)
    puzzle.empty(3, 3)
    
    puzzle_grid_list = []
    for row in puzzle.board:
        puzzle_grid_list.append([cell if cell is not None else 0 for cell in row])
    
    solver = SudokuGenerator(3, 3, board=puzzle.board)
    solution_grid_list = []
    for row in solver.board:
        solution_grid_list.append([cell if cell is not None else 0 for cell in row])
    
    sudoku = Sudoku.objects.create(
        difficulty=difficulty,
        puzzle_grid=puzzle_grid_list,
        solution_grid=solution_grid_list,
    )
    
    return redirect("detail", pk=sudoku.pk)
