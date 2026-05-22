from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import List

from src.buch.router.dependencies import get_autor_service
from src.buch.entity.autor_entity import Autor, AutorCreate, AutorUpdate
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


@router.post("/", response_model=Autor, status_code=status.HTTP_201_CREATED)
def create_autor(autor: AutorCreate, service: AutorService = Depends(get_autor_service)):
    return service.create(autor)


@router.put("/{autor_id}", response_model=Autor)
def update_autor(autor_id: int, autor: AutorCreate, service: AutorService = Depends(get_autor_service)):
    updated_autor = service.update(autor_id, autor)
    if not updated_autor:
        raise HTTPException(status_code=404, detail="Autor not found")
    return updated_autor


@router.patch("/{autor_id}", response_model=Autor)
def patch_autor(autor_id: int, autor: AutorUpdate, service: AutorService = Depends(get_autor_service)):
    patched_autor = service.patch(autor_id, autor)
    if not patched_autor:
        raise HTTPException(status_code=404, detail="Autor not found")
    return patched_autor


@router.delete("/{autor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_autor(autor_id: int, service: AutorService = Depends(get_autor_service)):
    deleted = service.delete(autor_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Autor not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
