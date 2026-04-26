import json

from fastapi import Depends
import pytest

from datetime import date
from sqlmodel import create_engine, Session, SQLModel, select
from app.core.config import settings
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionDep, get_db_session
from app.models.book import Book
from app.models.user import User, UserRole
from app.schemas.book import BookCreate
from app.schemas.user import UserRegister, UserUpdate
from app.core.security import get_current_user

engine = create_engine(settings.dev_db_connection_str)

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

    with open("/home/juanjo/proyects/BookClubMS/backend/test_books_to_create.json", "r") as f:
        data = json.load(f)
        for book_dict in data:
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
