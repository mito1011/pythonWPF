from typing import List, Optional

from src.book.entity.author_entity import Author, AuthorCreate, AuthorUpdate
from src.book.repository.author_repository import AuthorSQLiteRepo, author_repo


class AuthorService:
    def __init__(self, author_repo: AuthorSQLiteRepo):
        self.author_repo = author_repo

    def get_all(self) -> List[Author]:
        return self.author_repo.get_all()

    def get_by_id(self, author_id: int) -> Optional[Author]:
        return self.author_repo.get_by_id(author_id)

    def create(self, author_in: AuthorCreate) -> Author:
        return self.author_repo.create(author_in)

    def update(self, author_id: int, author_in: AuthorCreate) -> Optional[Author]:
        return self.author_repo.update(author_id, author_in)

    def patch(self, author_id: int, author_in: AuthorUpdate) -> Optional[Author]:
        return self.author_repo.patch(author_id, author_in)

    def delete(self, author_id: int) -> bool:
        return self.author_repo.delete(author_id)


author_service = AuthorService(author_repo=author_repo)
