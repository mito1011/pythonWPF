from src.buch.service.book_service import BookService, book_service
from src.buch.service.autor_service import AutorService, autor_service
from src.buch.service.verlag_service import VerlagService, verlag_service


def get_book_service() -> BookService:
    return book_service


def get_autor_service() -> AutorService:
    return autor_service


def get_verlag_service() -> VerlagService:
    return verlag_service
