import uuid
from django.db import models


ADJECTIVES = [
    "Happy", "Clever", "Brave", "Gentle", "Swift", "Bright", "Calm", "Kind",
    "Wise", "Bold", "Fair", "Keen", "Lively", "Merry", "Noble", "Proud",
    "Silly", "Warm", "Young", "Zesty", "Cool", "Eager", "Free", "Graceful",
    "Honest", "Joyful", "Kindly", "Lucky", "Mellow", "Nice", "Open", "Peaceful",
    "Quiet", "Rich", "Smooth", "Tender", "Unique", "Vivid", "Witty", "Zealous",
]

NOUNS = [
    "Panda", "Fox", "Owl", "Bear", "Wolf", "Hawk", "Deer", "Lion",
    "Tiger", "Eagle", "Dolphin", "Penguin", "Koala", "Otter", "Rabbit",
    "Swan", "Frog", "Turtle", "Whale", "Shark", "Seal", "Moose", "Elk",
    "Buffalo", "Crane", "Heron", "Loon", "Jay", "Wren", "Sparrow", "Finch",
    "Raven", "Crow", "Hare", "Mole", "Vole", "Badger", "Lynx",
    "Bobcat", "Cougar", "Jaguar", "Leopard", "Panther", "Cheetah", "Gazelle",
]


def generate_sudoku_name():
    uid = uuid.uuid4().int
    adj_idx = uid % len(ADJECTIVES)
    noun_idx = (uid // len(ADJECTIVES)) % len(NOUNS)
    return f"{ADJECTIVES[adj_idx]} {NOUNS[noun_idx]}"


class Sudoku(models.Model):
    DIFFICULTY_CHOICES = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),
        ("Extreme", "Extreme"),
    ]

    name = models.CharField(max_length=100, default=generate_sudoku_name)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default="Easy")
    puzzle_grid = models.JSONField()
    solution_grid = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.difficulty})"

    def get_puzzle_list(self):
        return self.puzzle_grid

    def get_solution_list(self):
        return self.solution_grid
