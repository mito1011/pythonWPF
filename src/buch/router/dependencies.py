from typing import Callable
from src.buch.repository.mock_repo import repo


def get_book_repo() -> Callable:
    return repo
