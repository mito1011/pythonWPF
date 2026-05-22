from src.buch.router.book_router import router as book_router
from src.buch.router.book_write_router import router as book_write_router
from src.buch.router.health_router import router as health_router
from src.buch.router.page import router as page_router
from src.buch.router.author_router import router as author_router
from src.buch.router.publisher_router import router as publisher_router

__all__ = ["book_router", "book_write_router", "health_router", "page_router", "author_router", "publisher_router"]
