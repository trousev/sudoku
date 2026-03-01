from django.core.management.base import BaseCommand
from sudokus.models import Sudoku


DIFFICULTY_TO_GIVENS = {
    "Easy": 45,
    "Medium": 35,
    "Hard": 25,
    "Extreme": 17,
}


class Command(BaseCommand):
    help = "Generate a new Sudoku puzzle"

    def add_arguments(self, parser):
        parser.add_argument(
            "--difficulty",
            type=str,
            default="Easy",
            choices=["Easy", "Medium", "Hard", "Extreme"],
            help="Difficulty level of the sudoku",
        )
        parser.add_argument(
            "--count",
            type=int,
            default=1,
            help="Number of sudokus to generate",
        )

    def handle(self, *args, **options):
        difficulty = options["difficulty"]
        count = options["count"]

        for i in range(count):
            self._generate_sudoku(difficulty)
            last = Sudoku.objects.order_by('-id').first()
            self.stdout.write(
                self.style.SUCCESS(f"Generated Sudoku: {last.name}")
            )

    def _generate_sudoku(self, difficulty):
        from sudoku import Sudoku as SudokuGenerator
        from sudokus.models import generate_sudoku_name
        import random
        
        name = generate_sudoku_name()
        self.stdout.write(f"  Generated name: {name}")

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

        Sudoku.objects.create(
            name=name,
            difficulty=difficulty,
            puzzle_grid=puzzle_grid_list,
            solution_grid=solution_grid_list,
        )
