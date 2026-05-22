from typing import Callable
from src.buch.repository.mock_repo import repo, autor_repo, verlag_repo


def get_book_repo() -> Callable:
    return repo


def get_autor_repo() -> Callable:
    return autor_repo


def get_verlag_repo() -> Callable:
    return verlag_repo
