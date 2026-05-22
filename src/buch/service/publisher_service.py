from typing import List, Optional

from src.buch.entity.publisher_entity import Publisher, PublisherCreate, PublisherUpdate
from src.buch.repository.sqlite_repo import PublisherSQLiteRepo
from src.buch.repository.sqlite_repo import publisher_repo


class PublisherService:
    def __init__(self, publisher_repo: PublisherSQLiteRepo):
        self.publisher_repo = publisher_repo

    def get_all(self) -> List[Publisher]:
        return self.publisher_repo.get_all()

    def get_by_id(self, publisher_id: int) -> Optional[Publisher]:
        return self.publisher_repo.get_by_id(publisher_id)

    def create(self, publisher_in: PublisherCreate) -> Publisher:
        return self.publisher_repo.create(publisher_in)

    def update(self, publisher_id: int, publisher_in: PublisherCreate) -> Optional[Publisher]:
        return self.publisher_repo.update(publisher_id, publisher_in)

    def patch(self, publisher_id: int, publisher_in: PublisherUpdate) -> Optional[Publisher]:
        return self.publisher_repo.patch(publisher_id, publisher_in)

    def delete(self, publisher_id: int) -> bool:
        return self.publisher_repo.delete(publisher_id)


publisher_service = PublisherService(publisher_repo=publisher_repo)
