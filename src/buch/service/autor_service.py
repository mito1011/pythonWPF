from typing import List, Optional

from src.buch.entity.autor_entity import Autor, AutorCreate
from src.buch.repository.mock_repo import AutorMockRepo
from src.buch.repository.mock_repo import autor_repo

class AutorService:
    def __init__(self, autor_repo: AutorMockRepo):
        self.autor_repo = autor_repo

    def get_all(self) -> List[Autor]:
        return self.autor_repo.get_all()

    def get_by_id(self, autor_id: int) -> Optional[Autor]:
        return self.autor_repo.get_by_id(autor_id)

    def create(self, autor_in: AutorCreate) -> Autor:
        return self.autor_repo.create(autor_in)



autor_service = AutorService(autor_repo=autor_repo)
