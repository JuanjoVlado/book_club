import random

from app.models.book import BookStatus
from app.schemas.user_book import UserBookUpdate


### GET ALL
def test_get_userbooks_success(test_client, userbooks_created):
    user_id = userbooks_created["user_id"]
    user_books = userbooks_created["userbooks"]

    response = test_client.get(f"/users/{user_id}/books/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(user_books)

def test_get_userbooks_invalid_user_id(test_client, userbooks_created):
    user_id = userbooks_created["user_id"]
    
    response = test_client.get(f"/users/{user_id+1}/books")
    assert response.status_code == 404
    
### GET BY ID
def test_get_userbook_by_id_success(test_client, userbooks_created):
    user_id = userbooks_created["user_id"]
    db_userbook = random.choice(userbooks_created["userbooks"])
    db_book_id = db_userbook["book_id"]

    response = test_client.get(f"/users/{user_id}/books/{db_book_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["book_id"] == db_book_id

def test_get_userbook_by_id_invalid_user_id(test_client, userbooks_created):
    user_id = userbooks_created["user_id"]
    db_userbook = random.choice(userbooks_created["userbooks"])
    db_book_id = db_userbook["book_id"]

    response = test_client.get(f"/users/{user_id+1}/books/{db_book_id}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == f"User with id {user_id+1} not found"

def test_get_userbook_by_id_book_not_found(test_client, userbooks_created):
    user_id = userbooks_created["user_id"]
    db_userbook = userbooks_created["userbooks"][-1]
    db_book_id = db_userbook["book_id"]

    response = test_client.get(f"/users/{user_id}/books/{db_book_id+1}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == f"Book with id {db_book_id+1} not found for User with id {user_id}"

### CREATE
def test_create_userbook_forbidden_user(test_client, books_created, register_regular_user):
    user = register_regular_user["user_id"]
    book = random.choice(books_created)

    response = test_client.post(
        f"/users/{user+1}/books/{book["id"]}",
        headers={"Authorization": f"Bearer {register_regular_user["access_token"]}"}
    )

    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "You can only add books to your own user account."

def test_create_userbook_book_not_found(test_client, books_created, register_regular_user):
    max_book_id = max(books_created, key=lambda x: x["id"])["id"]
    user_id = register_regular_user["user_id"]

    response = test_client.post(
        f"/users/{user_id}/books/{max_book_id+1}",
        headers={"Authorization": f"Bearer {register_regular_user["access_token"]}"}
    )

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == f"Could not find book with id {max_book_id+1}"

def test_create_userbook_duplicated(test_client, books_created, register_regular_user):
    book_id = random.choice(books_created)["id"]
    user_id = register_regular_user["user_id"]

    response = test_client.post(
        f"/users/{user_id}/books/{book_id}",
        headers={"Authorization": f"Bearer {register_regular_user["access_token"]}"}
    )

    assert response.status_code == 201

    response = test_client.post(
        f"/users/{user_id}/books/{book_id}",
        headers={"Authorization": f"Bearer {register_regular_user["access_token"]}"}
    )

    assert response.status_code == 409
    assert response.json()["detail"] == f"The book with id {book_id} is already associated with the user with id {user_id}"

### UPDATE
def test_update_userbook_success(test_client, userbooks_created):
    user_id = userbooks_created["user_id"]
    book_id = random.choice(userbooks_created["userbooks"])["book_id"]

    updated_userbook = UserBookUpdate(
        status= BookStatus.COMPLETED,
        notes="Book completed. Was good."
    )

    response = test_client.patch(
        f"/users/{user_id}/books/{book_id}",
        json=updated_userbook.model_dump(mode="json", exclude_unset=True),
        headers={"Authorization": f"Bearer {userbooks_created["access_token"]}"}
    )

    assert response.status_code == 200

    response = test_client.get(f"/users/{user_id}/books/{book_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == BookStatus.COMPLETED
    assert data["notes"] == "Book completed. Was good."

def test_update_userbook_forbidden_user(test_client, userbooks_created, register_regular_user):
    user_id = userbooks_created["user_id"]
    book_id = random.choice(userbooks_created["userbooks"])["book_id"]

    updated_userbook = UserBookUpdate(
        status= BookStatus.COMPLETED,
        notes="Book completed. Was good."
    )

    response = test_client.patch(
        f"/users/{user_id}/books/{book_id}",
        json=updated_userbook.model_dump(mode="json", exclude_unset=True),
        headers={"Authorization": f"Bearer {register_regular_user["access_token"]}"}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "You are not authorized to modify other user's books"


def test_update_userbook_book_not_found(test_client, userbooks_created):
    user_id = userbooks_created["user_id"]
    max_book_id = max(userbooks_created["userbooks"], key=lambda x: x["book_id"])["book_id"]

    updated_userbook = UserBookUpdate(
        status= BookStatus.COMPLETED,
        notes="Book completed. Was good."
    )

    response = test_client.patch(
        f"/users/{user_id}/books/{max_book_id+1}",
        json=updated_userbook.model_dump(mode="json", exclude_unset=True),
        headers={"Authorization": f"Bearer {userbooks_created["access_token"]}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Could not find the combination of User with id {user_id} and Book with id {max_book_id+1}"

### DELETE
def test_delete_userbook_success(test_client, userbooks_created):
    user_id = userbooks_created["user_id"]
    book_id = random.choice(userbooks_created["userbooks"])["book_id"]

    response = test_client.delete(
        f"/users/{user_id}/books/{book_id}",
        headers={"Authorization": f"Bearer {userbooks_created["access_token"]}"}
    )

    assert response.status_code == 200

    response = test_client.get(f"/users/{user_id}/books/{book_id}")
    assert response.status_code == 404

def test_delete_userbook_forbidden_user(test_client, userbooks_created, register_regular_user):
    user_id = userbooks_created["user_id"]
    book_id = random.choice(userbooks_created["userbooks"])["book_id"]

    response = test_client.delete(
        f"/users/{user_id}/books/{book_id}",
        headers={"Authorization": f"Bearer {register_regular_user["access_token"]}"}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "You are not authorized to modify other user's books"

def test_delete_userbook_not_found(test_client, userbooks_created):
    user_id = userbooks_created["user_id"]
    max_book_id = max(userbooks_created["userbooks"], key=lambda x: x["book_id"])["book_id"]

    response = test_client.delete(
        f"/users/{user_id}/books/{max_book_id+1}",
        headers={"Authorization": f"Bearer {userbooks_created["access_token"]}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Could not find the combination of User with id {user_id} and Book with id {max_book_id+1}"

