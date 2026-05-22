from pydantic import BaseModel
from typing import Optional


class Verlag(BaseModel):
    id: int
    name: str
    stadt: Optional[str] = None
    land: Optional[str] = None
    gruendungsjahr: Optional[int] = None


class VerlagCreate(BaseModel):
    name: str
    stadt: Optional[str] = None
    land: Optional[str] = None
    gruendungsjahr: Optional[int] = None
