import sqlite3
from typing import List, Optional

from src.buch.entity.publisher_entity import Publisher, PublisherCreate, PublisherUpdate
from src.buch.repository.database import SQLiteDatabase, database


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


publisher_repo = PublisherSQLiteRepo(database)
