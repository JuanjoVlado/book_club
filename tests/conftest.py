import pytest

from datetime import date
from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db_session
from app.schemas.user import UserRegister

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
    