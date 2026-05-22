from pydantic import BaseModel
from typing import Optional
from .autor_entity import Autor
from .verlag_entity import Verlag


class Book(BaseModel):
    id: int
    title: str
    autor: Autor
    verlag: Verlag
    description: Optional[str] = None
    publikationsjahr: Optional[int] = None


class BookCreate(BaseModel):
    title: str
    autor_id: int
    verlag_id: int
    description: Optional[str] = None
    publikationsjahr: Optional[int] = None
