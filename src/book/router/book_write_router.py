from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.book.router.dependencies import get_book_service
from src.book.entity.book_entity import BookCreate, Book, BookUpdate
from src.book.service.book_service import BookService

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book_in: BookCreate, service: BookService = Depends(get_book_service)):
    try:
        return service.create(book_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, book_in: BookCreate, service: BookService = Depends(get_book_service)):
    try:
        book = service.update(book_id, book_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.patch("/{book_id}", response_model=Book)
def patch_book(book_id: int, book_in: BookUpdate, service: BookService = Depends(get_book_service)):
    try:
        book = service.patch(book_id, book_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, service: BookService = Depends(get_book_service)):
    deleted = service.delete(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
