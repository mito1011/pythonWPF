import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, List, Optional

from src.buch.entity.author_entity import Author, AuthorCreate, AuthorUpdate
from src.buch.entity.book_entity import Book, BookCreate, BookUpdate
from src.buch.entity.publisher_entity import Publisher, PublisherCreate, PublisherUpdate


class SQLiteDatabase:
    def __init__(self, path: str = "data/books.sqlite3"):
        self.path = Path(os.environ.get("BUCH_DB_PATH", path))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()
        self._migrate_schema()
        self._seed_data()

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _init_schema(self) -> None:
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS authors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    birth_year INTEGER,
                    nationality TEXT
                );

                CREATE TABLE IF NOT EXISTS publishers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    city TEXT,
                    country TEXT,
                    founding_year INTEGER
                );

                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author_id INTEGER NOT NULL,
                    publisher_id INTEGER NOT NULL,
                    description TEXT,
                    publication_year INTEGER,
                    FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE RESTRICT,
                    FOREIGN KEY (publisher_id) REFERENCES publishers(id) ON DELETE RESTRICT
                );
                """
            )

    def _migrate_schema(self) -> None:
        with self.connect() as connection:
            # Keep local databases from earlier versions usable after the English rename.
            self._rename_columns(
                connection,
                "authors",
                {
                    "vorname": "first_name",
                    "geburtsjahr": "birth_year",
                    "nationalitaet": "nationality",
                },
            )
            self._rename_columns(
                connection,
                "publishers",
                {
                    "stadt": "city",
                    "land": "country",
                    "gruendungsjahr": "founding_year",
                },
            )
            self._rename_columns(
                connection,
                "books",
                {
                    "autor_id": "author_id",
                    "verlag_id": "publisher_id",
                    "publikationsjahr": "publication_year",
                },
            )

    def _rename_columns(self, connection: sqlite3.Connection, table: str, columns: dict[str, str]) -> None:
        existing_columns = {
            row["name"]
            for row in connection.execute(f"PRAGMA table_info({table})").fetchall()
        }
        for old_name, new_name in columns.items():
            if old_name in existing_columns and new_name not in existing_columns:
                connection.execute(f"ALTER TABLE {table} RENAME COLUMN {old_name} TO {new_name}")
                existing_columns.remove(old_name)
                existing_columns.add(new_name)

    def _seed_data(self) -> None:
        with self.connect() as connection:
            author_count = connection.execute("SELECT COUNT(*) FROM authors").fetchone()[0]
            publisher_count = connection.execute("SELECT COUNT(*) FROM publishers").fetchone()[0]
            book_count = connection.execute("SELECT COUNT(*) FROM books").fetchone()[0]

            if author_count == 0:
                connection.executemany(
                    """
                    INSERT INTO authors (id, name, first_name, birth_year, nationality)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    [
                        (1, "Saint-Exupéry", "Antoine de", 1900, "French"),
                        (2, "Goethe", "Johann Wolfgang von", 1749, "German"),
                    ],
                )

            if publisher_count == 0:
                connection.executemany(
                    """
                    INSERT INTO publishers (id, name, city, country, founding_year)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    [
                        (1, "Gallimard", "Paris", "France", 1911),
                        (2, "Suhrkamp", "Frankfurt am Main", "Germany", 1950),
                    ],
                )

            if book_count == 0:
                connection.executemany(
                    """
                    INSERT INTO books (id, title, author_id, publisher_id, description, publication_year)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    [
                        (1, "The Little Prince", 1, 1, "Classic", 1943),
                        (2, "Faust", 2, 2, "Drama", 1808),
                    ],
                )


class AuthorSQLiteRepo:
    def __init__(self, database: SQLiteDatabase):
        self.database = database

    def _row_to_author(self, row: sqlite3.Row) -> Author:
        return Author(
            id=row["id"],
            name=row["name"],
            first_name=row["first_name"],
            birth_year=row["birth_year"],
            nationality=row["nationality"],
        )

    def get_all(self) -> List[Author]:
        with self.database.connect() as connection:
            rows = connection.execute("SELECT * FROM authors ORDER BY id").fetchall()
            return [self._row_to_author(row) for row in rows]

    def get_by_id(self, author_id: int) -> Optional[Author]:
        with self.database.connect() as connection:
            row = connection.execute("SELECT * FROM authors WHERE id = ?", (author_id,)).fetchone()
            return self._row_to_author(row) if row else None

    def create(self, author_in: AuthorCreate) -> Author:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO authors (name, first_name, birth_year, nationality)
                VALUES (?, ?, ?, ?)
                """,
                (author_in.name, author_in.first_name, author_in.birth_year, author_in.nationality),
            )
            author_id = cursor.lastrowid
        author = self.get_by_id(author_id)
        if author is None:
            raise RuntimeError("Created author could not be loaded")
        return author

    def update(self, author_id: int, author_in: AuthorCreate) -> Optional[Author]:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                UPDATE authors
                SET name = ?, first_name = ?, birth_year = ?, nationality = ?
                WHERE id = ?
                """,
                (author_in.name, author_in.first_name, author_in.birth_year, author_in.nationality, author_id),
            )
            if cursor.rowcount == 0:
                return None
        return self.get_by_id(author_id)

    def patch(self, author_id: int, author_in: AuthorUpdate) -> Optional[Author]:
        author = self.get_by_id(author_id)
        if not author:
            return None

        data = author_in.model_dump(exclude_unset=True)
        if not data:
            return author

        allowed_fields = {"name", "first_name", "birth_year", "nationality"}
        assignments = ", ".join(f"{field} = ?" for field in data if field in allowed_fields)
        values = [value for field, value in data.items() if field in allowed_fields] + [author_id]
        with self.database.connect() as connection:
            connection.execute(f"UPDATE authors SET {assignments} WHERE id = ?", values)
        return self.get_by_id(author_id)

    def delete(self, author_id: int) -> bool:
        try:
            with self.database.connect() as connection:
                cursor = connection.execute("DELETE FROM authors WHERE id = ?", (author_id,))
                return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False


class PublisherSQLiteRepo:
    def __init__(self, database: SQLiteDatabase):
        self.database = database

    def _row_to_publisher(self, row: sqlite3.Row) -> Publisher:
        return Publisher(
            id=row["id"],
            name=row["name"],
            city=row["city"],
            country=row["country"],
            founding_year=row["founding_year"],
        )

    def get_all(self) -> List[Publisher]:
        with self.database.connect() as connection:
            rows = connection.execute("SELECT * FROM publishers ORDER BY id").fetchall()
            return [self._row_to_publisher(row) for row in rows]

    def get_by_id(self, publisher_id: int) -> Optional[Publisher]:
        with self.database.connect() as connection:
            row = connection.execute("SELECT * FROM publishers WHERE id = ?", (publisher_id,)).fetchone()
            return self._row_to_publisher(row) if row else None

    def create(self, publisher_in: PublisherCreate) -> Publisher:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO publishers (name, city, country, founding_year)
                VALUES (?, ?, ?, ?)
                """,
                (publisher_in.name, publisher_in.city, publisher_in.country, publisher_in.founding_year),
            )
            publisher_id = cursor.lastrowid
        publisher = self.get_by_id(publisher_id)
        if publisher is None:
            raise RuntimeError("Created publisher could not be loaded")
        return publisher

    def update(self, publisher_id: int, publisher_in: PublisherCreate) -> Optional[Publisher]:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                UPDATE publishers
                SET name = ?, city = ?, country = ?, founding_year = ?
                WHERE id = ?
                """,
                (publisher_in.name, publisher_in.city, publisher_in.country, publisher_in.founding_year, publisher_id),
            )
            if cursor.rowcount == 0:
                return None
        return self.get_by_id(publisher_id)

    def patch(self, publisher_id: int, publisher_in: PublisherUpdate) -> Optional[Publisher]:
        publisher = self.get_by_id(publisher_id)
        if not publisher:
            return None

        data = publisher_in.model_dump(exclude_unset=True)
        if not data:
            return publisher

        allowed_fields = {"name", "city", "country", "founding_year"}
        assignments = ", ".join(f"{field} = ?" for field in data if field in allowed_fields)
        values = [value for field, value in data.items() if field in allowed_fields] + [publisher_id]
        with self.database.connect() as connection:
            connection.execute(f"UPDATE publishers SET {assignments} WHERE id = ?", values)
        return self.get_by_id(publisher_id)

    def delete(self, publisher_id: int) -> bool:
        try:
            with self.database.connect() as connection:
                cursor = connection.execute("DELETE FROM publishers WHERE id = ?", (publisher_id,))
                return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False


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


database = SQLiteDatabase()
author_repo = AuthorSQLiteRepo(database)
publisher_repo = PublisherSQLiteRepo(database)
repo = BookSQLiteRepo(database, author_repo, publisher_repo)
