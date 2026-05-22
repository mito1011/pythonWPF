from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from src.buch.router import book_router, book_write_router, health_router, page_router, author_router, publisher_router

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="WPF Book API",
    description="A FastAPI project with REST endpoints and SQLite persistence.",
    version="0.1.0",
)

app.include_router(page_router)
app.include_router(book_router)
app.include_router(book_write_router)
app.include_router(health_router)
app.include_router(author_router)
app.include_router(publisher_router)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
