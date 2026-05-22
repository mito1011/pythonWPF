from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.buch.router.dependencies import get_verlag_service
from src.buch.entity.verlag_entity import Verlag, VerlagCreate
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


@router.post("/", response_model=Verlag)
def create_verlag(verlag: VerlagCreate, service: VerlagService = Depends(get_verlag_service)):
    return service.create(verlag)
