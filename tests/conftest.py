import pytest
from collections.abc import Generator
from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db_session

engine = create_engine(settings.dev_db_connection_str)

@pytest.fixture
def test_client():
    def override():
        with Session(engine) as session:
            SQLModel.metadata.drop_all(engine)
            SQLModel.metadata.create_all(engine)
            yield session

    app.dependency_overrides[get_db_session] = override
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()
