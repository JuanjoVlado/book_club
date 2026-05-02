import json
import random
import pytest

from pathlib import Path
from fastapi import Depends, HTTPException
from fastapi.testclient import TestClient
from datetime import date
from sqlmodel import create_engine, Session, SQLModel, select

from app.main import app
from app.db.session import SessionDep, get_db_session
from app.core.config import settings
from app.core.security import get_current_user
from app.models.book import Book
from app.models.club import BookClub
from app.models.club_user import ClubUser
from app.models.user import User, UserRole
from app.models.user_book import UserBook
from app.schemas.book import BookCreate
from app.schemas.club import ClubCreate
from app.schemas.user import UserRegister, UserUpdate

engine = create_engine(settings.dev_db_connection_str)
test_entities_path = Path(__file__).parent / "test_entities_to_create.json"

@pytest.fixture
def test_client():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    
    def override():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_db_session] = override
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()

@pytest.fixture
def registered_user(test_client):
    user = UserRegister(
        email="test_user@testing.com",
        password="TesTP@ssworD",
        name="Test User",
        date_of_birth=date(1991, 5, 9)
    )

    response = test_client.post("/auth/register", json=user.model_dump(mode="json"))

    if response.status_code == 201:
        data = response.json()
        yield {"user": user, "access_token": data["access_token"], "user_id": data["user_id"]}

@pytest.fixture
def register_regular_user(test_client):
    user = UserRegister(
        email="regular_user@testing.com",
        password="TesT_regular_P@ssworD",
        name="Regular User",
        date_of_birth=date(1991, 8, 12)
    )

    response = test_client.post("/auth/register", json=user.model_dump(mode="json"))

    if response.status_code == 201:
        data = response.json()
        yield {"user": user, "access_token": data["access_token"], "user_id": data["user_id"]}

@pytest.fixture
def admin_user(test_client, registered_user):
    user = registered_user["user"]
    with Session(engine) as session:
        statement = select(User).where(User.email == user.email)
        db_user = session.exec(statement).first()
        updateUser = UserUpdate(role=UserRole.ADMIN)
        db_user.sqlmodel_update(updateUser.model_dump(exclude_unset=True))
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        yield {"user": user, "access_token": registered_user["access_token"]}

@pytest.fixture
def books_created(test_client, admin_user):
    books = []

    with open(test_entities_path, "r") as f:
        data = json.load(f)
        for book_dict in data["books"]:
            book = BookCreate(
                title=book_dict["title"],
                author=book_dict["author"],
                description=book_dict["description"],
                editorial=book_dict["editorial"],
                genre=book_dict["genre"],
                isbn=book_dict["isbn"],
                page_count=book_dict["page_count"]
            )
            response = test_client.post(
                "/books/",
                json=book.model_dump(mode="json"),
                headers={"Authorization": f"Bearer {admin_user["access_token"]}"}
            )

            if response.status_code != 201:
                print(f"Unable to create {book.title} for testig. Skipped")
                continue
            
            books.append(response.json())
    
    yield books

@pytest.fixture
def create_clubs(test_client, admin_user):
    clubs = []

    with open(test_entities_path, "r") as f:
        data = json.load(f)
        for book_dict in data["clubs"]:
            club = ClubCreate(**book_dict)
            
            response = test_client.post(
                "/clubs/",
                json=club.model_dump(mode="json"),
                headers={"Authorization": f"Bearer {admin_user["access_token"]}"}
            )

            if response.status_code != 201:
                print(f"Unable to create {club.name} for testig. Skipped")
                continue
            
            clubs.append(response.json())
    
    yield {"clubs": clubs, "access_token": admin_user["access_token"]}
            
@pytest.fixture
def userbooks_created(test_client, registered_user, books_created):
    books_to_assign = random.sample(books_created, k=3)
    user_id = registered_user["user_id"]
    user_books = []

    for book in books_to_assign:
        userbook = UserBook(
            user_id=user_id,
            book_id=book["id"],
            notes=f"This is the book with id {book["id"]}"
        )

        response = test_client.post(
            f"/users/{userbook.user_id}/books/{userbook.book_id}",
            json=userbook.model_dump(mode="json"),
            headers={"Authorization": f"Bearer {registered_user["access_token"]}"}
        )

        if response.status_code != 201:
            print(f"Unable to create userbook {userbook.user_id}:{userbook.book_id} for testing. Skiped.")
            continue

        user_books.append(response.json())
    
    yield {"user_id": user_id, "userbooks": user_books, "access_token": registered_user["access_token"]}

@pytest.fixture
def users_created(test_client):
    users = []
    with open(test_entities_path, "r") as f:
        data = json.load(f)
        for user_dict in data["users"]:
            user = UserRegister(
                email=user_dict["email"],
                name=user_dict["name"],
                password=user_dict["password"],
                date_of_birth=user_dict["date_of_birth"],
            )

            response = test_client.post(
                f"/auth/register",
                json=user.model_dump(mode="json")
            )

            if response.status_code != 201:
                print(f"Unable to create User u:{user.name} for testing")
                pytest.fail(reason=response.json()["detail"])
            
            users.append(response.json())
    
    yield {"users": users}

@pytest.fixture
def club_user_created(test_client, create_clubs, users_created):
    club_users = []
    club = random.choice(create_clubs["clubs"])
    max_club_id = max(create_clubs["clubs"], key=lambda x: x["id"])["id"]
    users = users_created["users"]
    
    for user in users:
        response = test_client.post(
            f"/clubs/{club["id"]}/users/{user["user_id"]}",
            headers={"Authorization": f"Bearer {create_clubs["access_token"]}"}
        )

        if response.status_code != 201:
            print(f"Unable to create ClubUser c:{club["id"]} u:{user["user_id"]} for testing. Skipped.")
            continue
        
        club_users.append(response.json())

    yield {
        "club_id": club["id"],
        "clubs": create_clubs["clubs"],
        "users": users_created["users"],
        "clubusers": club_users,
        "access_token": create_clubs["access_token"]
    }

@pytest.fixture
def club_books_created(test_client, create_clubs, books_created):
    club_books = []
    club = random.choice(create_clubs["clubs"])

    for book in books_created:
        response = test_client.post(
            f"/clubs/{club["id"]}/books/{book["id"]}",
            headers={"Authorization": f"Bearer {create_clubs["access_token"]}"}
        )

        if response.status_code != 201:
            print(f"Unable to create ClubBook({club["id"]}, {book["id"]}) for testing. Skipped.")
            continue

        club_books.append(response.json())

    yield {
        "clubs": create_clubs["clubs"],
        "club_id": club["id"],
        "books": books_created,
        "club_books": club_books,
        "access_token": create_clubs["access_token"]
    }
