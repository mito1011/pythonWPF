from src.book.service.book_service import BookService, book_service
from src.book.service.author_service import AuthorService, author_service
from src.book.service.publisher_service import PublisherService, publisher_service


def get_book_service() -> BookService:
    return book_service


def get_author_service() -> AuthorService:
    return author_service


def get_publisher_service() -> PublisherService:
    return publisher_service
