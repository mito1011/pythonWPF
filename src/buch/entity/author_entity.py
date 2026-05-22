from pydantic import BaseModel
from typing import Optional


class Author(BaseModel):
    id: int
    name: str
    first_name: str
    birth_year: Optional[int] = None
    nationality: Optional[str] = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.name}"


class AuthorCreate(BaseModel):
    name: str
    first_name: str
    birth_year: Optional[int] = None
    nationality: Optional[str] = None


class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    first_name: Optional[str] = None
    birth_year: Optional[int] = None
    nationality: Optional[str] = None
