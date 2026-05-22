from typing import List, Optional
from src.buch.entity.buch_entity import Book, BookCreate
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.buch.router.buch_update_model import BookUpdate


class BookMockRepo:
    def __init__(self):
        self._books: List[Book] = [
            Book(id=1, title="Der kleine Prinz", author="Antoine de Saint-Exupéry", description="Klassiker"),
            Book(id=2, title="Faust", author="Johann Wolfgang von Goethe", description="Drama"),
        ]
        self._next = 3

    def get_all(self) -> List[Book]:
        return self._books

    def get_by_id(self, book_id: int) -> Optional[Book]:
        for b in self._books:
            if b.id == book_id:
                return b
        return None

    def create(self, book_in: BookCreate) -> Book:
        book = Book(id=self._next, title=book_in.title, author=book_in.author, description=book_in.description)
        self._books.append(book)
        self._next += 1
        return book

    def update(self, book_id: int, book_in: BookCreate) -> Optional[Book]:
        book = self.get_by_id(book_id)
        if not book:
            return None
        book.title = book_in.title
        book.author = book_in.author
        book.description = book_in.description
        return book

    def patch(self, book_id: int, book_in: "BookUpdate") -> Optional[Book]:
        book = self.get_by_id(book_id)
        if not book:
            return None
        if book_in.title is not None:
            book.title = book_in.title
        if book_in.author is not None:
            book.author = book_in.author
        if book_in.description is not None:
            book.description = book_in.description
        return book

    def delete(self, book_id: int) -> bool:
        book = self.get_by_id(book_id)
        if not book:
            return False
        self._books = [b for b in self._books if b.id != book_id]
        return True


repo = BookMockRepo()
