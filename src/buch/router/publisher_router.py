from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import List

from src.buch.router.dependencies import get_publisher_service
from src.buch.entity.publisher_entity import Publisher, PublisherCreate, PublisherUpdate
from src.buch.repository.errors import ReferencedEntityError
from src.buch.service.publisher_service import PublisherService

router = APIRouter(prefix="/publishers", tags=["Publishers"])


@router.get("/", response_model=List[Publisher])
def list_publishers(service: PublisherService = Depends(get_publisher_service)):
    return service.get_all()


@router.get("/{publisher_id}", response_model=Publisher)
def get_publisher(publisher_id: int, service: PublisherService = Depends(get_publisher_service)):
    publisher = service.get_by_id(publisher_id)
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return publisher


@router.post("/", response_model=Publisher, status_code=status.HTTP_201_CREATED)
def create_publisher(publisher: PublisherCreate, service: PublisherService = Depends(get_publisher_service)):
    return service.create(publisher)


@router.put("/{publisher_id}", response_model=Publisher)
def update_publisher(
    publisher_id: int,
    publisher: PublisherCreate,
    service: PublisherService = Depends(get_publisher_service),
):
    updated_publisher = service.update(publisher_id, publisher)
    if not updated_publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return updated_publisher


@router.patch("/{publisher_id}", response_model=Publisher)
def patch_publisher(
    publisher_id: int,
    publisher: PublisherUpdate,
    service: PublisherService = Depends(get_publisher_service),
):
    patched_publisher = service.patch(publisher_id, publisher)
    if not patched_publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return patched_publisher


@router.delete("/{publisher_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_publisher(publisher_id: int, service: PublisherService = Depends(get_publisher_service)):
    try:
        deleted = service.delete(publisher_id)
    except ReferencedEntityError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    if not deleted:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
