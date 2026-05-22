import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


class SQLiteDatabase:
    def __init__(self, path: str = "data/books.sqlite3"):
        self.path = Path(os.environ.get("book_DB_PATH", path))
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


database = SQLiteDatabase()
