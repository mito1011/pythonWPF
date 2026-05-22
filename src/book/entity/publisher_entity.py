from pydantic import BaseModel
from typing import Optional


class Publisher(BaseModel):
    id: int
    name: str
    city: Optional[str] = None
    country: Optional[str] = None
    founding_year: Optional[int] = None


class PublisherCreate(BaseModel):
    name: str
    city: Optional[str] = None
    country: Optional[str] = None
    founding_year: Optional[int] = None


class PublisherUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    founding_year: Optional[int] = None
