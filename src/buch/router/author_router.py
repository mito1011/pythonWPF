from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import List

from src.buch.router.dependencies import get_author_service
from src.buch.entity.author_entity import Author, AuthorCreate, AuthorUpdate
from src.buch.repository.errors import ReferencedEntityError
from src.buch.service.author_service import AuthorService

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get("/", response_model=List[Author])
def list_authors(service: AuthorService = Depends(get_author_service)):
    return service.get_all()


@router.get("/{author_id}", response_model=Author)
def get_author(author_id: int, service: AuthorService = Depends(get_author_service)):
    author = service.get_by_id(author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.post("/", response_model=Author, status_code=status.HTTP_201_CREATED)
def create_author(author: AuthorCreate, service: AuthorService = Depends(get_author_service)):
    return service.create(author)


@router.put("/{author_id}", response_model=Author)
def update_author(author_id: int, author: AuthorCreate, service: AuthorService = Depends(get_author_service)):
    updated_author = service.update(author_id, author)
    if not updated_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return updated_author


@router.patch("/{author_id}", response_model=Author)
def patch_author(author_id: int, author: AuthorUpdate, service: AuthorService = Depends(get_author_service)):
    patched_author = service.patch(author_id, author)
    if not patched_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return patched_author


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, service: AuthorService = Depends(get_author_service)):
    try:
        deleted = service.delete(author_id)
    except ReferencedEntityError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    if not deleted:
        raise HTTPException(status_code=404, detail="Author not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
