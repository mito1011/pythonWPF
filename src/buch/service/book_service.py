from typing import List, Optional

from src.buch.entity.book_entity import Book, BookCreate, BookUpdate
from src.buch.repository.author_repository import AuthorSQLiteRepo, author_repo
from src.buch.repository.book_repository import BookSQLiteRepo, repo as book_repo
from src.buch.repository.publisher_repository import PublisherSQLiteRepo, publisher_repo

class BookService:
    def __init__(self, book_repo: BookSQLiteRepo, author_repo: AuthorSQLiteRepo, publisher_repo: PublisherSQLiteRepo):
        self.book_repo = book_repo
        self.author_repo = author_repo
        self.publisher_repo = publisher_repo

    def get_all(self) -> List[Book]:
        return self.book_repo.get_all()

    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self.book_repo.get_by_id(book_id)

    def create(self, book_in: BookCreate) -> Book:
        author = self.author_repo.get_by_id(book_in.author_id)
        publisher = self.publisher_repo.get_by_id(book_in.publisher_id)
        if not author:
            raise ValueError("Author not found")
        if not publisher:
            raise ValueError("Publisher not found")
        return self.book_repo.create(book_in)

    def update(self, book_id: int, book_in: BookCreate) -> Optional[Book]:
        author = self.author_repo.get_by_id(book_in.author_id)
        publisher = self.publisher_repo.get_by_id(book_in.publisher_id)
        if not author:
            raise ValueError("Author not found")
        if not publisher:
            raise ValueError("Publisher not found")
        return self.book_repo.update(book_id, book_in)

    def patch(self, book_id: int, book_in: BookUpdate) -> Optional[Book]:
        if book_in.author_id is not None:
            author = self.author_repo.get_by_id(book_in.author_id)
            if not author:
                raise ValueError("Author not found")
        if book_in.publisher_id is not None:
            publisher = self.publisher_repo.get_by_id(book_in.publisher_id)
            if not publisher:
                raise ValueError("Publisher not found")
        return self.book_repo.patch(book_id, book_in)

    def delete(self, book_id: int) -> bool:
        return self.book_repo.delete(book_id)




book_service = BookService(book_repo=book_repo, author_repo=author_repo, publisher_repo=publisher_repo)
