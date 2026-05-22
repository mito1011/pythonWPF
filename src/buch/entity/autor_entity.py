from pydantic import BaseModel
from typing import Optional


class Autor(BaseModel):
    id: int
    name: str
    vorname: str
    geburtsjahr: Optional[int] = None
    nationalitaet: Optional[str] = None

    @property
    def full_name(self) -> str:
        return f"{self.vorname} {self.name}"


class AutorCreate(BaseModel):
    name: str
    vorname: str
    geburtsjahr: Optional[int] = None
    nationalitaet: Optional[str] = None
