import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, List, Optional

from src.buch.entity.autor_entity import Autor, AutorCreate, AutorUpdate
from src.buch.entity.buch_entity import Book, BookCreate, BookUpdate
from src.buch.entity.verlag_entity import Verlag, VerlagCreate, VerlagUpdate


class SQLiteDatabase:
    def __init__(self, path: str = "data/books.sqlite3"):
        self.path = Path(os.environ.get("BUCH_DB_PATH", path))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()
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
                    vorname TEXT NOT NULL,
                    geburtsjahr INTEGER,
                    nationalitaet TEXT
                );

                CREATE TABLE IF NOT EXISTS publishers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    stadt TEXT,
                    land TEXT,
                    gruendungsjahr INTEGER
                );

                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    autor_id INTEGER NOT NULL,
                    verlag_id INTEGER NOT NULL,
                    description TEXT,
                    publikationsjahr INTEGER,
                    FOREIGN KEY (autor_id) REFERENCES authors(id) ON DELETE RESTRICT,
                    FOREIGN KEY (verlag_id) REFERENCES publishers(id) ON DELETE RESTRICT
                );
                """
            )

    def _seed_data(self) -> None:
        with self.connect() as connection:
            author_count = connection.execute("SELECT COUNT(*) FROM authors").fetchone()[0]
            publisher_count = connection.execute("SELECT COUNT(*) FROM publishers").fetchone()[0]
            book_count = connection.execute("SELECT COUNT(*) FROM books").fetchone()[0]

            if author_count == 0:
                connection.executemany(
                    """
                    INSERT INTO authors (id, name, vorname, geburtsjahr, nationalitaet)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    [
                        (1, "Saint-Exupéry", "Antoine de", 1900, "Französisch"),
                        (2, "Goethe", "Johann Wolfgang von", 1749, "Deutsch"),
                    ],
                )

            if publisher_count == 0:
                connection.executemany(
                    """
                    INSERT INTO publishers (id, name, stadt, land, gruendungsjahr)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    [
                        (1, "Gallimard", "Paris", "Frankreich", 1911),
                        (2, "Suhrkamp", "Frankfurt am Main", "Deutschland", 1950),
                    ],
                )

            if book_count == 0:
                connection.executemany(
                    """
                    INSERT INTO books (id, title, autor_id, verlag_id, description, publikationsjahr)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    [
                        (1, "Der kleine Prinz", 1, 1, "Klassiker", 1943),
                        (2, "Faust", 2, 2, "Drama", 1808),
                    ],
                )


class AutorSQLiteRepo:
    def __init__(self, database: SQLiteDatabase):
        self.database = database

    def _row_to_autor(self, row: sqlite3.Row) -> Autor:
        return Autor(
            id=row["id"],
            name=row["name"],
            vorname=row["vorname"],
            geburtsjahr=row["geburtsjahr"],
            nationalitaet=row["nationalitaet"],
        )

    def get_all(self) -> List[Autor]:
        with self.database.connect() as connection:
            rows = connection.execute("SELECT * FROM authors ORDER BY id").fetchall()
            return [self._row_to_autor(row) for row in rows]

    def get_by_id(self, autor_id: int) -> Optional[Autor]:
        with self.database.connect() as connection:
            row = connection.execute("SELECT * FROM authors WHERE id = ?", (autor_id,)).fetchone()
            return self._row_to_autor(row) if row else None

    def create(self, autor_in: AutorCreate) -> Autor:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO authors (name, vorname, geburtsjahr, nationalitaet)
                VALUES (?, ?, ?, ?)
                """,
                (autor_in.name, autor_in.vorname, autor_in.geburtsjahr, autor_in.nationalitaet),
            )
            autor_id = cursor.lastrowid
        return self.get_by_id(autor_id)

    def update(self, autor_id: int, autor_in: AutorCreate) -> Optional[Autor]:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                UPDATE authors
                SET name = ?, vorname = ?, geburtsjahr = ?, nationalitaet = ?
                WHERE id = ?
                """,
                (autor_in.name, autor_in.vorname, autor_in.geburtsjahr, autor_in.nationalitaet, autor_id),
            )
            if cursor.rowcount == 0:
                return None
        return self.get_by_id(autor_id)

    def patch(self, autor_id: int, autor_in: AutorUpdate) -> Optional[Autor]:
        autor = self.get_by_id(autor_id)
        if not autor:
            return None

        data = autor_in.model_dump(exclude_unset=True)
        if not data:
            return autor

        assignments = ", ".join(f"{field} = ?" for field in data)
        values = list(data.values()) + [autor_id]
        with self.database.connect() as connection:
            connection.execute(f"UPDATE authors SET {assignments} WHERE id = ?", values)
        return self.get_by_id(autor_id)

    def delete(self, autor_id: int) -> bool:
        try:
            with self.database.connect() as connection:
                cursor = connection.execute("DELETE FROM authors WHERE id = ?", (autor_id,))
                return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False


class VerlagSQLiteRepo:
    def __init__(self, database: SQLiteDatabase):
        self.database = database

    def _row_to_verlag(self, row: sqlite3.Row) -> Verlag:
        return Verlag(
            id=row["id"],
            name=row["name"],
            stadt=row["stadt"],
            land=row["land"],
            gruendungsjahr=row["gruendungsjahr"],
        )

    def get_all(self) -> List[Verlag]:
        with self.database.connect() as connection:
            rows = connection.execute("SELECT * FROM publishers ORDER BY id").fetchall()
            return [self._row_to_verlag(row) for row in rows]

    def get_by_id(self, verlag_id: int) -> Optional[Verlag]:
        with self.database.connect() as connection:
            row = connection.execute("SELECT * FROM publishers WHERE id = ?", (verlag_id,)).fetchone()
            return self._row_to_verlag(row) if row else None

    def create(self, verlag_in: VerlagCreate) -> Verlag:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO publishers (name, stadt, land, gruendungsjahr)
                VALUES (?, ?, ?, ?)
                """,
                (verlag_in.name, verlag_in.stadt, verlag_in.land, verlag_in.gruendungsjahr),
            )
            verlag_id = cursor.lastrowid
        return self.get_by_id(verlag_id)

    def update(self, verlag_id: int, verlag_in: VerlagCreate) -> Optional[Verlag]:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                UPDATE publishers
                SET name = ?, stadt = ?, land = ?, gruendungsjahr = ?
                WHERE id = ?
                """,
                (verlag_in.name, verlag_in.stadt, verlag_in.land, verlag_in.gruendungsjahr, verlag_id),
            )
            if cursor.rowcount == 0:
                return None
        return self.get_by_id(verlag_id)

    def patch(self, verlag_id: int, verlag_in: VerlagUpdate) -> Optional[Verlag]:
        verlag = self.get_by_id(verlag_id)
        if not verlag:
            return None

        data = verlag_in.model_dump(exclude_unset=True)
        if not data:
            return verlag

        assignments = ", ".join(f"{field} = ?" for field in data)
        values = list(data.values()) + [verlag_id]
        with self.database.connect() as connection:
            connection.execute(f"UPDATE publishers SET {assignments} WHERE id = ?", values)
        return self.get_by_id(verlag_id)

    def delete(self, verlag_id: int) -> bool:
        try:
            with self.database.connect() as connection:
                cursor = connection.execute("DELETE FROM publishers WHERE id = ?", (verlag_id,))
                return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False


class BookSQLiteRepo:
    def __init__(self, database: SQLiteDatabase, autor_repo: AutorSQLiteRepo, verlag_repo: VerlagSQLiteRepo):
        self.database = database
        self.autor_repo = autor_repo
        self.verlag_repo = verlag_repo

    def _row_to_book(self, row: sqlite3.Row) -> Book:
        return Book(
            id=row["book_id"],
            title=row["title"],
            autor=Autor(
                id=row["autor_id"],
                name=row["autor_name"],
                vorname=row["autor_vorname"],
                geburtsjahr=row["autor_geburtsjahr"],
                nationalitaet=row["autor_nationalitaet"],
            ),
            verlag=Verlag(
                id=row["verlag_id"],
                name=row["verlag_name"],
                stadt=row["verlag_stadt"],
                land=row["verlag_land"],
                gruendungsjahr=row["verlag_gruendungsjahr"],
            ),
            description=row["description"],
            publikationsjahr=row["publikationsjahr"],
        )

    def _select_books_sql(self) -> str:
        return """
            SELECT
                books.id AS book_id,
                books.title,
                books.description,
                books.publikationsjahr,
                authors.id AS autor_id,
                authors.name AS autor_name,
                authors.vorname AS autor_vorname,
                authors.geburtsjahr AS autor_geburtsjahr,
                authors.nationalitaet AS autor_nationalitaet,
                publishers.id AS verlag_id,
                publishers.name AS verlag_name,
                publishers.stadt AS verlag_stadt,
                publishers.land AS verlag_land,
                publishers.gruendungsjahr AS verlag_gruendungsjahr
            FROM books
            JOIN authors ON authors.id = books.autor_id
            JOIN publishers ON publishers.id = books.verlag_id
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
                INSERT INTO books (title, autor_id, verlag_id, description, publikationsjahr)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    book_in.title,
                    book_in.autor_id,
                    book_in.verlag_id,
                    book_in.description,
                    book_in.publikationsjahr,
                ),
            )
            book_id = cursor.lastrowid
        return self.get_by_id(book_id)

    def update(self, book_id: int, book_in: BookCreate) -> Optional[Book]:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                UPDATE books
                SET title = ?, autor_id = ?, verlag_id = ?, description = ?, publikationsjahr = ?
                WHERE id = ?
                """,
                (
                    book_in.title,
                    book_in.autor_id,
                    book_in.verlag_id,
                    book_in.description,
                    book_in.publikationsjahr,
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

        assignments = ", ".join(f"{field} = ?" for field in data)
        values = list(data.values()) + [book_id]
        with self.database.connect() as connection:
            connection.execute(f"UPDATE books SET {assignments} WHERE id = ?", values)
        return self.get_by_id(book_id)

    def delete(self, book_id: int) -> bool:
        with self.database.connect() as connection:
            cursor = connection.execute("DELETE FROM books WHERE id = ?", (book_id,))
            return cursor.rowcount > 0


database = SQLiteDatabase()
autor_repo = AutorSQLiteRepo(database)
verlag_repo = VerlagSQLiteRepo(database)
repo = BookSQLiteRepo(database, autor_repo, verlag_repo)
