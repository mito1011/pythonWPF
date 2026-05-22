import sqlite3
from typing import List, Optional

from src.buch.entity.author_entity import Author
from src.buch.entity.book_entity import Book, BookCreate, BookUpdate
from src.buch.entity.publisher_entity import Publisher
from src.buch.repository.author_repository import AuthorSQLiteRepo, author_repo
from src.buch.repository.database import SQLiteDatabase, database
from src.buch.repository.publisher_repository import PublisherSQLiteRepo, publisher_repo


class BookSQLiteRepo:
    def __init__(self, database: SQLiteDatabase, author_repo: AuthorSQLiteRepo, publisher_repo: PublisherSQLiteRepo):
        self.database = database
        self.author_repo = author_repo
        self.publisher_repo = publisher_repo

    def _row_to_book(self, row: sqlite3.Row) -> Book:
        return Book(
            id=row["book_id"],
            title=row["title"],
            author=Author(
                id=row["author_id"],
                name=row["author_name"],
                first_name=row["author_first_name"],
                birth_year=row["author_birth_year"],
                nationality=row["author_nationality"],
            ),
            publisher=Publisher(
                id=row["publisher_id"],
                name=row["publisher_name"],
                city=row["publisher_city"],
                country=row["publisher_country"],
                founding_year=row["publisher_founding_year"],
            ),
            description=row["description"],
            publication_year=row["publication_year"],
        )

    def _select_books_sql(self) -> str:
        return """
            SELECT
                books.id AS book_id,
                books.title,
                books.description,
                books.publication_year,
                authors.id AS author_id,
                authors.name AS author_name,
                authors.first_name AS author_first_name,
                authors.birth_year AS author_birth_year,
                authors.nationality AS author_nationality,
                publishers.id AS publisher_id,
                publishers.name AS publisher_name,
                publishers.city AS publisher_city,
                publishers.country AS publisher_country,
                publishers.founding_year AS publisher_founding_year
            FROM books
            JOIN authors ON authors.id = books.author_id
            JOIN publishers ON publishers.id = books.publisher_id
        """

    def get_all(self) -> List[Book]:
        with self.database.connect() as connection:
            rows = connection.execute(f"{self._select_books_sql()} ORDER BY books.id").fetchall()
            return [self._row_to_book(row) for row in rows]

    def get_by_id(self, book_id: int) -> Optional[Book]:
        with self.database.connect() as connection:
            row = connection.execute(f"{self._select_books_sql()} WHERE books.id = ?", (book_id,)).fetchone()
            return self._row_to_book(row) if row else None

    def create(self, book_in: BookCreate) -> Book:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO books (title, author_id, publisher_id, description, publication_year)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    book_in.title,
                    book_in.author_id,
                    book_in.publisher_id,
                    book_in.description,
                    book_in.publication_year,
                ),
            )
            book_id = cursor.lastrowid
        book = self.get_by_id(book_id)
        if book is None:
            raise RuntimeError("Created book could not be loaded")
        return book

    def update(self, book_id: int, book_in: BookCreate) -> Optional[Book]:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                UPDATE books
                SET title = ?, author_id = ?, publisher_id = ?, description = ?, publication_year = ?
                WHERE id = ?
                """,
                (
                    book_in.title,
                    book_in.author_id,
                    book_in.publisher_id,
                    book_in.description,
                    book_in.publication_year,
                    book_id,
                ),
            )
            if cursor.rowcount == 0:
                return None
        return self.get_by_id(book_id)

    def patch(self, book_id: int, book_in: BookUpdate) -> Optional[Book]:
        book = self.get_by_id(book_id)
        if not book:
            return None

        data = book_in.model_dump(exclude_unset=True)
        if not data:
            return book

        allowed_fields = {"title", "author_id", "publisher_id", "description", "publication_year"}
        assignments = ", ".join(f"{field} = ?" for field in data if field in allowed_fields)
        values = [value for field, value in data.items() if field in allowed_fields] + [book_id]
        with self.database.connect() as connection:
            connection.execute(f"UPDATE books SET {assignments} WHERE id = ?", values)
        return self.get_by_id(book_id)

    def delete(self, book_id: int) -> bool:
        with self.database.connect() as connection:
            cursor = connection.execute("DELETE FROM books WHERE id = ?", (book_id,))
            return cursor.rowcount > 0


repo = BookSQLiteRepo(database, author_repo, publisher_repo)
