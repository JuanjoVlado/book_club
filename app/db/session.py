from collections.abc import Generator
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine

from app.core.config import settings

engine = create_engine(settings.db_connection_str)

def get_db_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db_session)]
