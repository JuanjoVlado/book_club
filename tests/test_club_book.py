import random
from app.models.book import BookStatus
from app.schemas.club_book import ClubBookUpdate

### CREATE
def test_create_ClubBook_success(test_client, create_clubs, books_created):
    club_id = random.choice(create_clubs["clubs"])["id"]
    book_id = random.choice(books_created)["id"]

    response = test_client.post(
        f"/clubs/{club_id}/books/{book_id}",
        headers={"Authorization": f"Bearer {create_clubs["access_token"]}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["club_id"] == club_id
    assert data["book_id"] == book_id

def test_create_ClubBook_forbidden(test_client, create_clubs, books_created, register_regular_user):
    club_id = random.choice(create_clubs["clubs"])["id"]
    book_id = random.choice(books_created)["id"]

    response = test_client.post(
        f"/clubs/{club_id}/books/{book_id}",
        headers={"Authorization": f"Bearer {register_regular_user["access_token"]}"}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "You do not have permission to perform this action."

def test_create_ClubBook_club_not_found(test_client, create_clubs, books_created):
    max_club_id = max(create_clubs["clubs"], key=lambda club: club["id"])["id"]
    book_id = random.choice(books_created)["id"]
    
    response = test_client.post(
        f"/clubs/{max_club_id+1}/books/{book_id}",
        headers={"Authorization": f"Bearer {create_clubs["access_token"]}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Club with id {max_club_id+1} not found"

def test_create_ClubBook_book_not_found(test_client, create_clubs, books_created):
    club_id = random.choice(create_clubs["clubs"])["id"]
    max_book_id = max(books_created, key=lambda book: book["id"])["id"]
    
    response = test_client.post(
        f"/clubs/{club_id}/books/{max_book_id+1}",
        headers={"Authorization": f"Bearer {create_clubs["access_token"]}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Book with id {max_book_id+1} not found"

def test_create_ClubBook_duplicated(test_client, club_books_created):
    club_id = club_books_created["club_id"]
    book_id = random.choice(club_books_created["books"])["id"]

    response = test_client.post(
        f"/clubs/{club_id}/books/{book_id}",
        headers={"Authorization": f"Bearer {club_books_created["access_token"]}"}
    )

    assert response.status_code == 409
    assert response.json()["detail"] == f"The Book with id {book_id} is already on Club with id {club_id}"

### GET
def test_get_all_ClubBook_success(test_client, club_books_created):
    club_id = club_books_created["club_id"]
    response = test_client.get(f"/clubs/{club_id}/books")

    assert response.status_code == 200
    assert len(response.json()) == len(club_books_created["clubs"])

def test_get_all_ClubBook_club_not_found(test_client, club_books_created):
    max_club_id = max(club_books_created["clubs"], key=lambda book: book["id"])["id"]
    response = test_client.get(f"/clubs/{max_club_id+1}/books")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Club with id {max_club_id+1} not found"

def test_get_ClubBook_by_id_success(test_client, club_books_created):
    club_id = club_books_created["club_id"]
    book_id = random.choice(club_books_created["books"])["id"]

    response = test_client.get(f"/clubs/{club_id}/books/{book_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["club_id"] == club_id
    assert data["book_id"] == book_id

def test_get_ClubBook_by_id_club_not_found(test_client, club_books_created):
    max_club_id = max(club_books_created["clubs"], key=lambda book: book["id"])["id"]
    book_id = random.choice(club_books_created["books"])["id"]

    response = test_client.get(f"/clubs/{max_club_id+1}/books/{book_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Club with id {max_club_id+1} not found"

def test_get_ClubBook_by_id_book_not_found(test_client, club_books_created):
    club_id = club_books_created["club_id"]
    max_book_id = max(club_books_created["books"], key=lambda book: book["id"])["id"]

    response = test_client.get(f"/clubs/{club_id}/books/{max_book_id+1}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Book with id {max_book_id+1} not found in Club with id {club_id}"

### UPDATE
def test_update_ClubBook_success(test_client, club_books_created):
    club_id = club_books_created["club_id"]
    book_id = random.choice(club_books_created["books"])["id"]

    updated_ClubBook = ClubBookUpdate(status=BookStatus.READING)

    response = test_client.patch(
        f"/clubs/{club_id}/books/{book_id}",
        json=updated_ClubBook.model_dump(mode="json", exclude_unset=True),
        headers={"Authorization": f"Bearer {club_books_created["access_token"]}"}
    )

    assert response.status_code == 202
    data = response.json()
    assert data["club_id"] == club_id
    assert data["book_id"] == book_id
    assert data["status"] == BookStatus.READING


def test_update_ClubBook_forbidden(test_client, club_books_created, register_regular_user):
    club_id = club_books_created["club_id"]
    book_id = random.choice(club_books_created["books"])["id"]

    updated_ClubBook = ClubBookUpdate(status=BookStatus.READING)

    response = test_client.patch(
        f"/clubs/{club_id}/books/{book_id}",
        json=updated_ClubBook.model_dump(mode="json", exclude_unset=True),
        headers={"Authorization": f"Bearer {register_regular_user["access_token"]}"}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "You do not have permission to perform this action."

def test_update_ClubBook_club_not_found(test_client, club_books_created):
    max_club_id = max(club_books_created["clubs"], key=lambda club: club["id"])["id"]
    book_id = random.choice(club_books_created["books"])["id"]

    updated_ClubBook = ClubBookUpdate(status=BookStatus.READING)

    response = test_client.patch(
        f"/clubs/{max_club_id+1}/books/{book_id}",
        json=updated_ClubBook.model_dump(mode="json", exclude_unset=True),
        headers={"Authorization": f"Bearer {club_books_created["access_token"]}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Club with id {max_club_id+1} not found"

def test_update_ClubBook_book_not_found(test_client, club_books_created):
    club_id = club_books_created["club_id"]
    max_book_id = max(club_books_created["books"], key=lambda book: book["id"])["id"]

    updated_ClubBook = ClubBookUpdate(status=BookStatus.READING)

    response = test_client.patch(
        f"/clubs/{club_id}/books/{max_book_id+1}",
        json=updated_ClubBook.model_dump(mode="json", exclude_unset=True),
        headers={"Authorization": f"Bearer {club_books_created["access_token"]}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Book with id {max_book_id+1} not found in Club with id {club_id}"

### DELETE
def test_delete_ClubBook_success(test_client, club_books_created):
    club_id = club_books_created["club_id"]
    book_id = random.choice(club_books_created["books"])["id"]

    response = test_client.delete(
        f"/clubs/{club_id}/books/{book_id}",
        headers={"Authorization": f"Bearer {club_books_created["access_token"]}"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Book with id {book_id} removed from Club with id {club_id}"

    response = test_client.get(f"/clubs/{club_id}/books/{book_id}")
    assert response.status_code == 404

def test_delete_ClubBook_forbidden(test_client, club_books_created, register_regular_user):
    club_id = club_books_created["club_id"]
    book_id = random.choice(club_books_created["books"])["id"]

    response = test_client.delete(
        f"/clubs/{club_id}/books/{book_id}",
        headers={"Authorization": f"Bearer {register_regular_user["access_token"]}"}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "You do not have permission to perform this action."

def test_delete_ClubBook_club_not_found(test_client, club_books_created):
    max_club_id = max(club_books_created["clubs"], key=lambda club: club["id"])["id"]
    book_id = random.choice(club_books_created["books"])["id"]

    response = test_client.delete(
        f"/clubs/{max_club_id+1}/books/{book_id}",
        headers={"Authorization": f"Bearer {club_books_created["access_token"]}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Club with id {max_club_id+1} not found"

def test_delete_ClubBook_book_not_found(test_client, club_books_created):
    club_id = club_books_created["club_id"]
    max_book_id = max(club_books_created["books"], key=lambda book: book["id"])["id"]

    response = test_client.delete(
        f"/clubs/{club_id}/books/{max_book_id+1}",
        headers={"Authorization": f"Bearer {club_books_created["access_token"]}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Book with id {max_book_id+1} not found in Club with id {club_id}"
