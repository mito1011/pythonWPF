from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.buch.router.dependencies import get_book_repo
from src.buch.entity.buch_entity import BookCreate, Book
from src.buch.repository.mock_repo import BookMockRepo
from src.buch.router.buch_update_model import BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book_in: BookCreate, repo: BookMockRepo = Depends(get_book_repo)):
    return repo.create(book_in)


@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, book_in: BookCreate, repo: BookMockRepo = Depends(get_book_repo)):
    book = repo.update(book_id, book_in)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.patch("/{book_id}", response_model=Book)
def patch_book(book_id: int, book_in: BookUpdate, repo: BookMockRepo = Depends(get_book_repo)):
    book = repo.patch(book_id, book_in)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, repo: BookMockRepo = Depends(get_book_repo)):
    deleted = repo.delete(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
