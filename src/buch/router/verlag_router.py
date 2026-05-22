from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.buch.router.dependencies import get_verlag_repo
from src.buch.entity.verlag_entity import Verlag, VerlagCreate
from src.buch.repository.mock_repo import VerlagMockRepo

router = APIRouter(prefix="/verlage", tags=["Verlage"])


@router.get("/", response_model=List[Verlag])
def list_verlage(repo: VerlagMockRepo = Depends(get_verlag_repo)):
    return repo.get_all()


@router.get("/{verlag_id}", response_model=Verlag)
def get_verlag(verlag_id: int, repo: VerlagMockRepo = Depends(get_verlag_repo)):
    v = repo.get_by_id(verlag_id)
    if not v:
        raise HTTPException(status_code=404, detail="Verlag not found")
    return v


@router.post("/", response_model=Verlag)
def create_verlag(verlag: VerlagCreate, repo: VerlagMockRepo = Depends(get_verlag_repo)):
    return repo.create(verlag)
