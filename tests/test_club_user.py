import random

from app.models.club_user import ClubUserStatus
from app.schemas.club_user import ClubUserUpdate


### GET
def test_get_all_club_users_success(test_client, club_user_created):
    response = test_client.get(f"/clubs/{club_user_created["club_id"]}/users")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(club_user_created["clubusers"])

def test_get_all_club_users_club_not_found(test_client, club_user_created):
    max_club_id = max(club_user_created["clubs"], key=lambda x: x["id"])["id"]
    response = test_client.get(f"/clubs/{max_club_id+1}/users")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Book Club with id {max_club_id+1} not found"

### GET BY ID
def test_get_club_user_by_id_success(test_client, club_user_created):
    db_club_id = club_user_created["club_id"]
    db_user = random.choice(club_user_created["clubusers"])

    response = test_client.get(f"/clubs/{db_club_id}/users/{db_user["user_id"]}")
    assert response.status_code == 200
    data = response.json()
    assert data["club_id"] == db_club_id
    assert data["user_id"] == db_user["user_id"]

def test_get_club_user_by_id_user_not_found(test_client, club_user_created):
    db_club_id = club_user_created["club_id"]
    max_user_id = max(club_user_created["users"], key=lambda x: x["user_id"])["user_id"]

    response = test_client.get(f"/clubs/{db_club_id}/users/{max_user_id+1}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"User with id {max_user_id+1} not found in Book Club with id {db_club_id}"

### CREATE
def test_create_club_user_success(test_client, users_created, create_clubs):
    db_user_id = random.choice(users_created["users"])["user_id"]
    db_club_id = random.choice(create_clubs["clubs"])["id"]

    response = test_client.post(
        f"/clubs/{db_club_id}/users/{db_user_id}",
        headers={"Authorization": f"Bearer {create_clubs["access_token"]}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["club_id"] == db_club_id
    assert data["user_id"] == db_user_id

def test_create_club_user_forbidden(test_client, users_created, create_clubs):
    db_user = random.choice(users_created["users"])
    db_club_id = random.choice(create_clubs["clubs"])["id"]

    response = test_client.post(
        f"/clubs/{db_club_id}/users/{db_user["user_id"]}",
        headers={"Authorization": f"Bearer {db_user["access_token"]}"}
    )

    assert response.status_code == 403

def test_create_club_user_club_not_found(test_client, users_created, create_clubs):
    max_club_id = max(create_clubs["clubs"], key=lambda x: x["id"])["id"]
    user_id = random.choice(users_created["users"])["user_id"]

    response = test_client.post(
        f"/clubs/{max_club_id+1}/users/{user_id}",
        headers={"Authorization": f"Bearer {create_clubs["access_token"]}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Club with id {max_club_id+1} not found"

def test_create_club_user_user_not_found(test_client, club_user_created):
    club_id = club_user_created["club_id"]
    max_user_id = max(club_user_created["users"], key=lambda x: x["user_id"])["user_id"]

    response = test_client.post(
        f"/clubs/{club_id}/users/{max_user_id+1}",
        headers={"Authorization": f"Bearer {club_user_created["access_token"]}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"User with id {max_user_id+1} not found."

def test_create_club_duplicated(test_client, club_user_created):
    db_clubuser = random.choice(club_user_created["clubusers"])

    response = test_client.post(
        f"/clubs/{club_user_created["club_id"]}/users/{db_clubuser["user_id"]}",
        headers={"Authorization": f"Bearer {club_user_created["access_token"]}"}
    )

    assert response.status_code == 409
    assert response.json()["detail"] == f"User with id {db_clubuser["user_id"]} is already a member of Club with id {club_user_created["club_id"]}"

### UPDATE
def test_update_club_user_success(test_client, club_user_created):
    db_clubuser = random.choice(club_user_created["clubusers"])
    update_clubuser = ClubUserUpdate(user_status=ClubUserStatus.INACTIVE)

    response = test_client.patch(
        f"/clubs/{db_clubuser["club_id"]}/users/{db_clubuser["user_id"]}",
        json=update_clubuser.model_dump(mode="json", exclude_unset=True),
        headers={"Authorization": f"Bearer {club_user_created["access_token"]}"}
    )

    assert response.status_code == 202
    assert response.json()["user_status"] == ClubUserStatus.INACTIVE

def test_update_club_user_forbidden(test_client, club_user_created):
    db_clubuser = random.choice(club_user_created["clubusers"])
    update_clubuser = ClubUserUpdate(user_status=ClubUserStatus.INACTIVE)
    user = random.choice(club_user_created["users"])

    response = test_client.patch(
        f"/clubs/{db_clubuser["club_id"]}/users/{db_clubuser["user_id"]}",
        json=update_clubuser.model_dump(mode="json", exclude_unset=True),
        headers={"Authorization": f"Bearer {user["access_token"]}"}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "You do not have permission to perform this action."

### DELETE
def test_delete_club_user_success(test_client, club_user_created):
    db_clubuser = random.choice(club_user_created["clubusers"])
    response = test_client.delete(
        f"/clubs/{db_clubuser["club_id"]}/users/{db_clubuser["user_id"]}",
        headers={"Authorization": f"Bearer {club_user_created["access_token"]}"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"User with id {db_clubuser["user_id"]} removed from Book Club with id {db_clubuser["club_id"]}"

    response = test_client.get(f"/clubs/{db_clubuser["club_id"]}/users/{db_clubuser["user_id"]}")
    assert response.status_code == 404    

def test_delete_club_user_forbidden(test_client, club_user_created):
    db_clubuser = random.choice(club_user_created["clubusers"])
    user = random.choice(club_user_created["users"])

    response = test_client.delete(
        f"/clubs/{db_clubuser["club_id"]}/users/{db_clubuser["user_id"]}",
        headers={"Authorization": f"Bearer {user["access_token"]}"}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "You do not have permission to perform this action."
