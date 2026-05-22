from typing import List, Optional

from src.buch.entity.buch_entity import Book, BookCreate, BookUpdate
from src.buch.repository.sqlite_repo import AutorSQLiteRepo, BookSQLiteRepo, VerlagSQLiteRepo
from src.buch.repository.sqlite_repo import autor_repo, repo as book_repo, verlag_repo

class BookService:
    def __init__(self, book_repo: BookSQLiteRepo, autor_repo: AutorSQLiteRepo, verlag_repo: VerlagSQLiteRepo):
        self.book_repo = book_repo
        self.autor_repo = autor_repo
        self.verlag_repo = verlag_repo

    def get_all(self) -> List[Book]:
        return self.book_repo.get_all()

    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self.book_repo.get_by_id(book_id)

    def create(self, book_in: BookCreate) -> Book:
        autor = self.autor_repo.get_by_id(book_in.autor_id)
        verlag = self.verlag_repo.get_by_id(book_in.verlag_id)
        if not autor:
            raise ValueError("Author not found")
        if not verlag:
            raise ValueError("Publisher not found")
        return self.book_repo.create(book_in)

    def update(self, book_id: int, book_in: BookCreate) -> Optional[Book]:
        autor = self.autor_repo.get_by_id(book_in.autor_id)
        verlag = self.verlag_repo.get_by_id(book_in.verlag_id)
        if not autor:
            raise ValueError("Author not found")
        if not verlag:
            raise ValueError("Publisher not found")
        return self.book_repo.update(book_id, book_in)

    def patch(self, book_id: int, book_in: BookUpdate) -> Optional[Book]:
        if hasattr(book_in, "autor_id") and book_in.autor_id is not None:
            autor = self.autor_repo.get_by_id(book_in.autor_id)
            if not autor:
                raise ValueError("Author not found")
        if hasattr(book_in, "verlag_id") and book_in.verlag_id is not None:
            verlag = self.verlag_repo.get_by_id(book_in.verlag_id)
            if not verlag:
                raise ValueError("Publisher not found")
        return self.book_repo.patch(book_id, book_in)

    def delete(self, book_id: int) -> bool:
        return self.book_repo.delete(book_id)




book_service = BookService(book_repo=book_repo, autor_repo=autor_repo, verlag_repo=verlag_repo)
