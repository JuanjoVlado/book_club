import random

from sqlmodel import SQLModel

from app.models.club import BookClub
from app.schemas.club import ClubCreate, ClubUpdate

def test_create_club_success(test_client, registered_user):
    club = ClubCreate(name="Test Club", description="A Book Club that serves as a test.")

    response = test_client.post(
        "/clubs/",
        json=club.model_dump(mode="json"),
        headers={"Authorization": f"Bearer {registered_user["access_token"]}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == club.name
    assert data["description"] == club.description

def test_create_club_missing_fields(test_client, registered_user):
    response = test_client.post(
        "/clubs/",
        json={"description": "A Book Club that serves as a test."},
        headers={"Authorization": f"Bearer {registered_user["access_token"]}"}
    )

    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["type"] == "missing"

def test_create_club_duplicated_name(test_client, create_clubs):
    club = random.choice(create_clubs["clubs"])

    response = test_client.post(
        "/clubs/",
        json=club,
        headers={"Authorization": f"Bearer {create_clubs["access_token"]}"}
    )

    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == f"There is a Club named {club["name"]} already. Choose a different name for your club."


def test_get_all_clubs_success(test_client, create_clubs):
    response = test_client.get("/clubs/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(create_clubs["clubs"])

def test_get_club_by_id_success(test_client, create_clubs):
    club_to_get = random.choice(create_clubs["clubs"])

    response = test_client.get(f"/clubs/{club_to_get["id"]}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == club_to_get["name"]

def test_get_club_by_id_invalid_id(test_client, create_clubs):
    invalid_id = max(create_clubs["clubs"], key=lambda x: x["id"])
    invalid_id = invalid_id["id"] + 1

    response = test_client.get(f"/clubs/{invalid_id}")

    assert response.status_code == 404


def test_update_club_success(test_client, create_clubs):
    club = random.choice(create_clubs["clubs"])
    updated_club = ClubUpdate(
        name=f"{club["name"]} Updated Name"
    )

    response = test_client.patch(
        f"/clubs/{club["id"]}",
        json=updated_club.model_dump(mode="json", exclude_unset=True),
        headers={"Authorization": f"Bearer {create_clubs["access_token"]}"}
    )

    assert response.status_code == 202
    data = response.json()
    assert data["id"] == club["id"]
    assert data["name"] == f"{club["name"]} Updated Name"
    assert data["description"] == club["description"]


def test_update_club_no_admin(test_client, create_clubs, register_regular_user):
    club = random.choice(create_clubs["clubs"])
    updated_club = ClubUpdate(
        name=f"{club["name"]} Updated Name"
    )

    response = test_client.patch(
        f"/clubs/{club["id"]}",
        json=updated_club.model_dump(mode="json", exclude_unset=True),
        headers={"Authorization": f"Bearer {register_regular_user["access_token"]}"}
    )

    assert response.status_code == 403

def test_delete_club_success(test_client, create_clubs):
    club_to_delete = random.choice(create_clubs["clubs"])
    
    response = test_client.delete(
        f"/clubs/{club_to_delete["id"]}",
        headers={"Authorization": f"Bearer {create_clubs["access_token"]}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == f"Club {club_to_delete["name"]} deleted."

    response = test_client.get(f"/clubs/{club_to_delete["id"]}")
    assert response.status_code == 404

def test_delete_club_no_admin(test_client, create_clubs, register_regular_user):
    club_to_delete = random.choice(create_clubs["clubs"])
    
    response = test_client.delete(
        f"/clubs/{club_to_delete["id"]}",
        headers={"Authorization": f"Bearer {register_regular_user["access_token"]}"}
    )

    assert response.status_code == 403

def test_delete_club_invalid_id(test_client, create_clubs):
    invalid_id = max(create_clubs["clubs"], key=lambda x: x["id"])["id"] + 1

    response = test_client.delete(
        f"/clubs/{invalid_id}",
        headers={"Authorization": f"Bearer {create_clubs["access_token"]}"}
    )

    assert response.status_code == 404
