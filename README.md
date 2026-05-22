# FastAPI-Projekt

Dieses Projekt enthält ein einfaches FastAPI-Grundgerüst.

## Vorbereitung

1. Installiere die Abhängigkeiten mit `uv`:

```bash
uv sync --dev
```

`uv` erstellt dabei automatisch die virtuelle Umgebung `.venv`.

## Projektlayout

Das Projekt folgt dem `src/buch`-Layout mit einfachem MVC-Pattern:

- `src/buch/entity` — Entitätsklassen (Pydantic)
- `src/buch/service` — Geschäftslogik
- `src/buch/repository` — SQLite-Repositories / Datenzugriff
- `src/buch/router` — REST-Controller (APIRouter)
- `src/buch/templates` — Jinja2-Templates (Views)
- `src/buch/static` — statische Assets

## Starten der Anwendung

```bash
uv run uvicorn src.buch.main:app --reload
```

Die API ist dann unter `http://127.0.0.1:8000` erreichbar.

Die Anwendung nutzt standardmäßig eine SQLite-Datenbank unter `data/books.sqlite3`.
Beim ersten Start werden Tabellen und Beispieldaten automatisch angelegt.
Für einen anderen Datenbankpfad kann die Umgebungsvariable `BUCH_DB_PATH` gesetzt werden.

## Beispiel-Endpunkte

- `GET /`
- `GET /books`
- `GET /books/{book_id}`
- `POST /books`
- `PUT /books/{book_id}`
- `PATCH /books/{book_id}`
- `DELETE /books/{book_id}`
- `GET /authors`
- `POST /authors`
- `PUT /authors/{author_id}`
- `PATCH /authors/{author_id}`
- `DELETE /authors/{author_id}`
- `GET /publishers`
- `POST /publishers`
- `PUT /publishers/{publisher_id}`
- `PATCH /publishers/{publisher_id}`
- `DELETE /publishers/{publisher_id}`
- `GET /books/view`

Swagger UI: `http://127.0.0.1:8000/docs`

## Tests

```bash
uv run pytest
```
