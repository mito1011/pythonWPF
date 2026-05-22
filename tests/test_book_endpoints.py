from fastapi.testclient import TestClient

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
    assert response.json()["title"] == "Der kleine Prinz"


def test_create_update_patch_and_delete_book():
    create_response = client.post(
        "/books/",
        json={
            "title": "CRUD Test Buch",
            "autor_id": 1,
            "verlag_id": 1,
            "description": "Created in test",
            "publikationsjahr": 2026,
        },
    )

    assert create_response.status_code == 201
    created_book = create_response.json()
    book_id = created_book["id"]
    assert created_book["title"] == "CRUD Test Buch"
    assert created_book["autor"]["id"] == 1
    assert created_book["verlag"]["id"] == 1

    update_response = client.put(
        f"/books/{book_id}",
        json={
            "title": "CRUD Test Buch Updated",
            "autor_id": 2,
            "verlag_id": 2,
            "description": "Updated in test",
            "publikationsjahr": 2025,
        },
    )

    assert update_response.status_code == 200
    updated_book = update_response.json()
    assert updated_book["title"] == "CRUD Test Buch Updated"
    assert updated_book["autor"]["id"] == 2
    assert updated_book["verlag"]["id"] == 2

    patch_response = client.patch(
        f"/books/{book_id}",
        json={"description": "Patched in test"},
    )

    assert patch_response.status_code == 200
    patched_book = patch_response.json()
    assert patched_book["description"] == "Patched in test"
    assert patched_book["title"] == "CRUD Test Buch Updated"

    delete_response = client.delete(f"/books/{book_id}")

    assert delete_response.status_code == 204
    assert client.get(f"/books/{book_id}").status_code == 404


def test_book_error_responses():
    assert client.get("/books/9999").status_code == 404

    invalid_create_response = client.post(
        "/books/",
        json={
            "title": "Invalid Book",
            "autor_id": 9999,
            "verlag_id": 1,
        },
    )

    assert invalid_create_response.status_code == 400

    invalid_patch_response = client.patch(
        "/books/1",
        json={"verlag_id": 9999},
    )

    assert invalid_patch_response.status_code == 400
