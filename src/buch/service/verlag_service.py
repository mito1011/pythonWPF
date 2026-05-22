from typing import List, Optional

from src.buch.entity.verlag_entity import Verlag, VerlagCreate
from src.buch.repository.mock_repo import VerlagMockRepo


class VerlagService:
    def __init__(self, verlag_repo: VerlagMockRepo):
        self.verlag_repo = verlag_repo

    def get_all(self) -> List[Verlag]:
        return self.verlag_repo.get_all()

    def get_by_id(self, verlag_id: int) -> Optional[Verlag]:
        return self.verlag_repo.get_by_id(verlag_id)

    def create(self, verlag_in: VerlagCreate) -> Verlag:
        return self.verlag_repo.create(verlag_in)


from src.buch.repository.mock_repo import verlag_repo
verlag_service = VerlagService(verlag_repo=verlag_repo)
