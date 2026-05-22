# FastAPI-Projekt

Dieses Projekt enthält ein einfaches FastAPI-Grundgerüst.

## Vorbereitung

1. Erstelle ein virtuelles Umfeld:

```bash
python -m venv .venv
```

2. Aktiviere das virtuelle Umfeld:

- PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```
- CMD:
```cmd
.\.venv\Scripts\activate.bat
```

3. Installiere die Abhängigkeiten:

```bash
pip install -r requirements.txt
```

## Projektlayout

Das Projekt folgt dem `src/buch`-Layout mit einfachem MVC-Pattern:

- `src/buch/entity` — Entitätsklassen (Pydantic)
- `src/buch/service` — Geschäftslogik
- `src/buch/repository` — Mock-Repositories / Datenzugriff
- `src/buch/router` — REST-Controller (APIRouter)
- `src/buch/templates` — Jinja2-Templates (Views)
- `src/buch/static` — statische Assets

## Starten der Anwendung

```bash
uvicorn src.buch.main:app --reload
```

Die API ist dann unter `http://127.0.0.1:8000` erreichbar.

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
