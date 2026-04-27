import json
import pytest

from pathlib import Path
from fastapi import Depends
from fastapi.testclient import TestClient
from datetime import date
from sqlmodel import create_engine, Session, SQLModel, select

from app.main import app
from app.db.session import SessionDep, get_db_session
from app.core.config import settings
from app.core.security import get_current_user
from app.models.book import Book
from app.models.club import BookClub
from app.models.user import User, UserRole
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
        access_token = response.json()["access_token"]
        yield {"user": user, "access_token": access_token}

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
        access_token = response.json()["access_token"]
        yield {"user": user, "access_token": access_token}

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
                page_count=book_dict["pages"]
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
            
