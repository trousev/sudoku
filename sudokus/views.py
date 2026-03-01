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


DIFFICULTY_TO_GIVENS = {
    "Easy": 45,
    "Medium": 35,
    "Hard": 25,
    "Extreme": 17,
}


def generate_sudoku(request, difficulty):
    from sudoku import Sudoku as SudokuGenerator
    import random
    
    givens = DIFFICULTY_TO_GIVENS.get(difficulty, 45)
    
    generator = SudokuGenerator(3, 3)
    solved = generator.solve()
    
    puzzle_board = [row[:] for row in solved.board]
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    for r, c in cells[:81-givens]:
        puzzle_board[r][c] = None
    
    puzzle_grid_list = []
    for row in puzzle_board:
        puzzle_grid_list.append([cell if cell is not None else 0 for cell in row])
    
    solution_grid_list = []
    for row in solved.board:
        solution_grid_list.append([cell if cell is not None else 0 for cell in row])
    
    from .models import Sudoku as SudokuModel
    sudoku = SudokuModel.objects.create(
        difficulty=difficulty,
        puzzle_grid=puzzle_grid_list,
        solution_grid=solution_grid_list,
    )
    
    return redirect("detail", pk=sudoku.pk)
