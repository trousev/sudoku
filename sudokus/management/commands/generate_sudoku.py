from django.core.management.base import BaseCommand
from sudokus.models import Sudoku


DIFFICULTY_TO_EMPTY = {
    "Easy": 30,
    "Medium": 40,
    "Hard": 50,
    "Extreme": 55,
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
        
        name = generate_sudoku_name()
        self.stdout.write(f"  Generated name: {name}")

        empty_blocks = DIFFICULTY_TO_EMPTY.get(difficulty, 30)
        generator = SudokuGenerator(3, 3)
        puzzle_grid = generator.board
        puzzle = SudokuGenerator(3, 3, board=puzzle_grid)
        puzzle.empty(3, 3)

        puzzle_grid_list = []
        for row in puzzle.board:
            puzzle_grid_list.append([cell if cell is not None else 0 for cell in row])

        solver = SudokuGenerator(3, 3, board=puzzle.board)
        solution_grid_list = []
        for row in solver.board:
            solution_grid_list.append([cell if cell is not None else 0 for cell in row])

        Sudoku.objects.create(
            name=name,
            difficulty=difficulty,
            puzzle_grid=puzzle_grid_list,
            solution_grid=solution_grid_list,
        )
