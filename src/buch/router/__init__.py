from src.buch.router.buch_router import router as buch_router
from src.buch.router.buch_write_router import router as buch_write_router
from src.buch.router.health_router import router as health_router
from src.buch.router.page import router as page_router

__all__ = ["buch_router", "buch_write_router", "health_router", "page_router"]
