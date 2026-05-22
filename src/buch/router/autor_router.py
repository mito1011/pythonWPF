from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.buch.router.dependencies import get_autor_repo
from src.buch.entity.autor_entity import Autor, AutorCreate
from src.buch.repository.mock_repo import AutorMockRepo

router = APIRouter(prefix="/autoren", tags=["Autoren"])


@router.get("/", response_model=List[Autor])
def list_autoren(repo: AutorMockRepo = Depends(get_autor_repo)):
    return repo.get_all()


@router.get("/{autor_id}", response_model=Autor)
def get_autor(autor_id: int, repo: AutorMockRepo = Depends(get_autor_repo)):
    a = repo.get_by_id(autor_id)
    if not a:
        raise HTTPException(status_code=404, detail="Autor not found")
    return a


@router.post("/", response_model=Autor)
def create_autor(autor: AutorCreate, repo: AutorMockRepo = Depends(get_autor_repo)):
    return repo.create(autor)
