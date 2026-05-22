from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import List

from src.buch.router.dependencies import get_verlag_service
from src.buch.entity.verlag_entity import Verlag, VerlagCreate, VerlagUpdate
from src.buch.service.verlag_service import VerlagService

router = APIRouter(prefix="/verlage", tags=["Verlage"])


@router.get("/", response_model=List[Verlag])
def list_verlage(service: VerlagService = Depends(get_verlag_service)):
    return service.get_all()


@router.get("/{verlag_id}", response_model=Verlag)
def get_verlag(verlag_id: int, service: VerlagService = Depends(get_verlag_service)):
    v = service.get_by_id(verlag_id)
    if not v:
        raise HTTPException(status_code=404, detail="Verlag not found")
    return v


@router.post("/", response_model=Verlag, status_code=status.HTTP_201_CREATED)
def create_verlag(verlag: VerlagCreate, service: VerlagService = Depends(get_verlag_service)):
    return service.create(verlag)


@router.put("/{verlag_id}", response_model=Verlag)
def update_verlag(verlag_id: int, verlag: VerlagCreate, service: VerlagService = Depends(get_verlag_service)):
    updated_verlag = service.update(verlag_id, verlag)
    if not updated_verlag:
        raise HTTPException(status_code=404, detail="Verlag not found")
    return updated_verlag


@router.patch("/{verlag_id}", response_model=Verlag)
def patch_verlag(verlag_id: int, verlag: VerlagUpdate, service: VerlagService = Depends(get_verlag_service)):
    patched_verlag = service.patch(verlag_id, verlag)
    if not patched_verlag:
        raise HTTPException(status_code=404, detail="Verlag not found")
    return patched_verlag


@router.delete("/{verlag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_verlag(verlag_id: int, service: VerlagService = Depends(get_verlag_service)):
    deleted = service.delete(verlag_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Verlag not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
