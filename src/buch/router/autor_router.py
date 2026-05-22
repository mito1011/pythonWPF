from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.buch.router.dependencies import get_autor_service
from src.buch.entity.autor_entity import Autor, AutorCreate
from src.buch.service.autor_service import AutorService

router = APIRouter(prefix="/autoren", tags=["Autoren"])


@router.get("/", response_model=List[Autor])
def list_autoren(service: AutorService = Depends(get_autor_service)):
    return service.get_all()


@router.get("/{autor_id}", response_model=Autor)
def get_autor(autor_id: int, service: AutorService = Depends(get_autor_service)):
    a = service.get_by_id(autor_id)
    if not a:
        raise HTTPException(status_code=404, detail="Autor not found")
    return a


@router.post("/", response_model=Autor)
def create_autor(autor: AutorCreate, service: AutorService = Depends(get_autor_service)):
    return service.create(autor)
