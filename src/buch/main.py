from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.buch.router import buch_router, buch_write_router, health_router, page_router, autor_router, verlag_router

app = FastAPI(
    title="WPF Abgabe (src/buch layout)",
    description="Ein FastAPI-Projekt, bei dem alle Anwendungsbestandteile unter src/buch liegen.",
    version="0.1.0",
)

app.include_router(page_router)
app.include_router(buch_router)
app.include_router(buch_write_router)
app.include_router(health_router)
app.include_router(autor_router)
app.include_router(verlag_router)

app.mount("/static", StaticFiles(directory="src/buch/static"), name="static")
