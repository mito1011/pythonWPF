from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from src.buch.router.dependencies import get_book_service
from src.buch.service.book_service import BookService

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parents[1]
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@router.get("/", response_class=HTMLResponse, tags=["Pages"])
def index(request: Request, service: BookService = Depends(get_book_service)):
    books = service.get_all()
    return templates.TemplateResponse(request, "index.html", {"request": request, "books": books})


@router.get("/books/view", response_class=HTMLResponse, tags=["Pages"])
def view_books(request: Request, service: BookService = Depends(get_book_service)):
    books = service.get_all()
    return templates.TemplateResponse(request, "books.html", {"request": request, "books": books})
