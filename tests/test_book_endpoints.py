import os
from pathlib import Path

from fastapi.testclient import TestClient

test_db_path = Path("data/test_books.sqlite3")
if test_db_path.exists():
    test_db_path.unlink()
os.environ["BUCH_DB_PATH"] = str(test_db_path)

from src.buch.main import app


client = TestClient(app)


def test_health_live():
    response = client.get("/health/live")

    assert response.status_code == 200


def test_list_and_get_books():
    response = client.get("/books/")

    assert response.status_code == 200
    books = response.json()
    assert isinstance(books, list)
    assert len(books) >= 2

    response = client.get("/books/1")

    assert response.status_code == 200
    assert response.json()["title"] == "The Little Prince"


def test_create_update_patch_and_delete_book():
    create_response = client.post(
        "/books/",
        json={
            "title": "CRUD Test Book",
            "author_id": 1,
            "publisher_id": 1,
            "description": "Created in test",
            "publication_year": 2026,
        },
    )

    assert create_response.status_code == 201
    created_book = create_response.json()
    book_id = created_book["id"]
    assert created_book["title"] == "CRUD Test Book"
    assert created_book["author"]["id"] == 1
    assert created_book["publisher"]["id"] == 1

    update_response = client.put(
        f"/books/{book_id}",
        json={
            "title": "CRUD Test Book Updated",
            "author_id": 2,
            "publisher_id": 2,
            "description": "Updated in test",
            "publication_year": 2025,
        },
    )

    assert update_response.status_code == 200
    updated_book = update_response.json()
    assert updated_book["title"] == "CRUD Test Book Updated"
    assert updated_book["author"]["id"] == 2
    assert updated_book["publisher"]["id"] == 2

    patch_response = client.patch(
        f"/books/{book_id}",
        json={"description": "Patched in test"},
    )

    assert patch_response.status_code == 200
    patched_book = patch_response.json()
    assert patched_book["description"] == "Patched in test"
    assert patched_book["title"] == "CRUD Test Book Updated"

    delete_response = client.delete(f"/books/{book_id}")

    assert delete_response.status_code == 204
    assert client.get(f"/books/{book_id}").status_code == 404


def test_book_error_responses():
    assert client.get("/books/9999").status_code == 404

    invalid_create_response = client.post(
        "/books/",
        json={
            "title": "Invalid Book",
            "author_id": 9999,
            "publisher_id": 1,
        },
    )

    assert invalid_create_response.status_code == 400

    invalid_patch_response = client.patch(
        "/books/1",
        json={"publisher_id": 9999},
    )

    assert invalid_patch_response.status_code == 400


def test_create_update_patch_and_delete_author():
    create_response = client.post(
        "/authors/",
        json={
            "name": "Mann",
            "first_name": "Thomas",
            "birth_year": 1875,
            "nationality": "German",
        },
    )

    assert create_response.status_code == 201
    created_author = create_response.json()
    author_id = created_author["id"]
    assert created_author["name"] == "Mann"

    update_response = client.put(
        f"/authors/{author_id}",
        json={
            "name": "Kafka",
            "first_name": "Franz",
            "birth_year": 1883,
            "nationality": "Czech",
        },
    )

    assert update_response.status_code == 200
    updated_author = update_response.json()
    assert updated_author["name"] == "Kafka"
    assert updated_author["first_name"] == "Franz"

    patch_response = client.patch(
        f"/authors/{author_id}",
        json={"nationality": "German-speaking"},
    )

    assert patch_response.status_code == 200
    patched_author = patch_response.json()
    assert patched_author["nationality"] == "German-speaking"
    assert patched_author["name"] == "Kafka"

    delete_response = client.delete(f"/authors/{author_id}")

    assert delete_response.status_code == 204
    assert client.get(f"/authors/{author_id}").status_code == 404


def test_author_error_responses():
    assert client.get("/authors/9999").status_code == 404

    update_response = client.put(
        "/authors/9999",
        json={
            "name": "Unknown",
            "first_name": "Nobody",
        },
    )

    assert update_response.status_code == 404
    assert client.patch("/authors/9999", json={"name": "Niemand"}).status_code == 404
    assert client.delete("/authors/9999").status_code == 404


def test_create_update_patch_and_delete_publisher():
    create_response = client.post(
        "/publishers/",
        json={
            "name": "Test Publisher",
            "city": "Berlin",
            "country": "Germany",
            "founding_year": 2000,
        },
    )

    assert create_response.status_code == 201
    created_publisher = create_response.json()
    publisher_id = created_publisher["id"]
    assert created_publisher["name"] == "Test Publisher"

    update_response = client.put(
        f"/publishers/{publisher_id}",
        json={
            "name": "Updated Publisher",
            "city": "Hamburg",
            "country": "Germany",
            "founding_year": 2001,
        },
    )

    assert update_response.status_code == 200
    updated_publisher = update_response.json()
    assert updated_publisher["name"] == "Updated Publisher"
    assert updated_publisher["city"] == "Hamburg"

    patch_response = client.patch(
        f"/publishers/{publisher_id}",
        json={"country": "DE"},
    )

    assert patch_response.status_code == 200
    patched_publisher = patch_response.json()
    assert patched_publisher["country"] == "DE"
    assert patched_publisher["name"] == "Updated Publisher"

    delete_response = client.delete(f"/publishers/{publisher_id}")

    assert delete_response.status_code == 204
    assert client.get(f"/publishers/{publisher_id}").status_code == 404


def test_publisher_error_responses():
    assert client.get("/publishers/9999").status_code == 404

    update_response = client.put(
        "/publishers/9999",
        json={
            "name": "Unknown Publisher",
        },
    )

    assert update_response.status_code == 404
    assert client.patch("/publishers/9999", json={"name": "Niemand"}).status_code == 404
    assert client.delete("/publishers/9999").status_code == 404
