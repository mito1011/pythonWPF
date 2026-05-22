from pydantic import BaseModel
from typing import Optional


class BookUpdate(BaseModel):
    title: Optional[str] = None
    autor_id: Optional[int] = None
    verlag_id: Optional[int] = None
    description: Optional[str] = None
    publikationsjahr: Optional[int] = None
