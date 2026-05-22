from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.buch.repository.mock_repo import repo

router = APIRouter()
templates = Jinja2Templates(directory="src/buch/templates")


@router.get("/", response_class=HTMLResponse, tags=["Pages"])
def index(request: Request):
    books = repo.get_all()
    return templates.TemplateResponse(request, "index.html", {"request": request, "books": books})


@router.get("/books/view", response_class=HTMLResponse, tags=["Pages"])
def view_books(request: Request):
    books = repo.get_all()
    return templates.TemplateResponse(request, "books.html", {"request": request, "books": books})
