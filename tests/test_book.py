import random

from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate

def test_book_create_successful(test_client, admin_user):
    book = BookCreate(
        title="El mundo y sus demonios. La ciencia como una luz en la oscuridad",
        author="Carl Sagan",
        editorial="Random House Publishing Group",
        description="El libro en general es una reflexión contra la pseudociencia, pero más específicamente, es una defensa profunda de los beneficios que la ciencia ha producido a lo largo de la historia (vacunas, antibióticos, medicamentos, aviación, etc.)",
        isbn="978-8416771486",
        genre=["biography", "reference"],
        page_count=457
    )
    
    response = test_client.post(
        "/books/",
        json=book.model_dump(mode="json"),
        headers={"Authorization": f"Bearer {admin_user["access_token"]}"}
    )

    assert response.status_code == 201

def test_book_create_missing_fields(test_client, admin_user):
    book = {
        #title="El mundo y sus demonios. La ciencia como una luz en la oscuridad",
        "author":"Carl Sagan",
        "editorial":"Random House Publishing Group",
        "description":"El libro en general es una reflexión contra la pseudociencia, pero más específicamente, es una defensa profunda de los beneficios que la ciencia ha producido a lo largo de la historia (vacunas, antibióticos, medicamentos, aviación, etc.)",
        "isbn":"978-8416771486",
        "genre":["biography", "reference"],
        "page_count":457
    }

    response = test_client.post(
        "/books/",
        json=book,
        headers={"Authorization": f"Bearer {admin_user["access_token"]}"}
    )

    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["type"] == "missing"

def test_book_create_duplicated_isbn(test_client, books_created, admin_user):
    dup_book = random.choice(books_created)

    response = test_client.post(
        "/books/",
        json=dup_book,
        headers={"Authorization": f"Bearer {admin_user["access_token"]}"}
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Book already exists"}

def test_book_get_all_success(test_client, books_created):
    response = test_client.get("/books/")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(books_created)

def test_book_get_by_id_success(test_client, books_created):
    book = random.choice(books_created)

    response = test_client.get(f"/books/{book["id"]}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == book["id"]

def test_book_get_by_id_invalid_id(test_client, books_created):
    max_id_book = max(books_created, key=lambda x: x["id"])
    response = test_client.get(f"/books/{max_id_book["id"] + 1}")

    assert response.status_code == 404
    
def test_book_edit_success(test_client, books_created, admin_user):
    book_to_update = random.choice(books_created)
    updated_book = BookUpdate(title="Título modificado", author="Autor modificado")

    response = test_client.patch(
        f"/books/{book_to_update["id"]}",
        json=updated_book.model_dump(mode="json", exclude_unset=True),
        headers={"Authorization": f"Bearer {admin_user["access_token"]}"}
    )

    assert response.status_code == 202
    data = response.json()
    assert data["id"] == book_to_update["id"]
    assert data["title"] == updated_book.title
    assert data["author"] == updated_book.author

def test_book_delete_success(test_client, books_created, admin_user):
    book_to_delete = random.choice(books_created)

    response = test_client.delete(
        f"/books/{book_to_delete["id"]}",
        headers={"Authorization": f"Bearer {admin_user["access_token"]}"}
    )

    assert response.status_code == 200
    assert response.json() == {"detail": "Book deleted"}

    response = test_client.get(f"/books/{book_to_delete["id"]}")
    assert response.status_code == 404