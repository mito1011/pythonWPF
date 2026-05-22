from typing import List, Optional

from src.buch.entity.verlag_entity import Verlag, VerlagCreate, VerlagUpdate
from src.buch.repository.sqlite_repo import VerlagSQLiteRepo


class VerlagService:
    def __init__(self, verlag_repo: VerlagSQLiteRepo):
        self.verlag_repo = verlag_repo

    def get_all(self) -> List[Verlag]:
        return self.verlag_repo.get_all()

    def get_by_id(self, verlag_id: int) -> Optional[Verlag]:
        return self.verlag_repo.get_by_id(verlag_id)

    def create(self, verlag_in: VerlagCreate) -> Verlag:
        return self.verlag_repo.create(verlag_in)

    def update(self, verlag_id: int, verlag_in: VerlagCreate) -> Optional[Verlag]:
        return self.verlag_repo.update(verlag_id, verlag_in)

    def patch(self, verlag_id: int, verlag_in: VerlagUpdate) -> Optional[Verlag]:
        return self.verlag_repo.patch(verlag_id, verlag_in)

    def delete(self, verlag_id: int) -> bool:
        return self.verlag_repo.delete(verlag_id)


from src.buch.repository.sqlite_repo import verlag_repo
verlag_service = VerlagService(verlag_repo=verlag_repo)
