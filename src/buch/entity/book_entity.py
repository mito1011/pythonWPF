from pydantic import BaseModel
from typing import Optional

from .author_entity import Author
from .publisher_entity import Publisher


class Book(BaseModel):
    id: int
    title: str
    author: Author
    publisher: Publisher
    description: Optional[str] = None
    publication_year: Optional[int] = None


class BookCreate(BaseModel):
    title: str
    author_id: int
    publisher_id: int
    description: Optional[str] = None
    publication_year: Optional[int] = None


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author_id: Optional[int] = None
    publisher_id: Optional[int] = None
    description: Optional[str] = None
    publication_year: Optional[int] = None
