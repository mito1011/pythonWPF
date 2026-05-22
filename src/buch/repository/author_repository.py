import sqlite3
from typing import List, Optional

from src.buch.entity.author_entity import Author, AuthorCreate, AuthorUpdate
from src.buch.repository.database import SQLiteDatabase, database


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


author_repo = AuthorSQLiteRepo(database)
