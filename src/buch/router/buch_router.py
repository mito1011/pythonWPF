from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.buch.router.dependencies import get_book_repo
from src.buch.entity.buch_entity import Book
from src.buch.repository.mock_repo import BookMockRepo

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[Book])
def list_books(repo: BookMockRepo = Depends(get_book_repo)):
    return repo.get_all()


@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, repo: BookMockRepo = Depends(get_book_repo)):
    b = repo.get_by_id(book_id)
    if not b:
        raise HTTPException(status_code=404, detail="Book not found")
    return b
