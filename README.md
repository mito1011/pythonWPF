# FastAPI-Projekt

Dieses Projekt enthält ein einfaches FastAPI-Grundgerüst.

## Vorbereitung

Voraussetzungen:

- Python >= 3.11
- `uv`

1. Installiere die Abhängigkeiten mit `uv`:

```bash
uv sync --dev
```

`uv` erstellt dabei automatisch die virtuelle Umgebung `.venv`.

## Projektlayout

Das Projekt folgt dem `src/buch`-Layout mit einfachem MVC-Pattern:

- `src/buch/entity` — Entity- und Request/Response-Modelle (Pydantic)
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
SQLite-Dateien unter `data/` werden nicht versioniert.

## Mailpit

Beim Anlegen eines Buchs kann die Anwendung optional eine E-Mail an Mailpit senden.
Die Funktion ist standardmäßig deaktiviert.

Mailpit mit Docker starten:

```bash
docker run --rm -p 8025:8025 -p 1025:1025 axllent/mailpit
```

App mit Mail-Benachrichtigung starten:

```bash
BUCH_EMAIL_ENABLED=true uv run uvicorn src.buch.main:app --reload
```

PowerShell:

```powershell
$env:BUCH_EMAIL_ENABLED = "true"
uv run uvicorn src.buch.main:app --reload
```

Mailpit UI: `http://127.0.0.1:8025`

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
