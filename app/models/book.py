from datetime import datetime
from enum import StrEnum
from typing import List
from sqlmodel import ARRAY, Column, Field, SQLModel, String


class BookStatus(StrEnum):
    COMPLETED = "completed"
    READING = "reading"
    PENDING = "pending"

class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author: str
    editorial: str
    description: str
    page_count: int
    isbn: str
    genre: List[str] = Field(sa_column=Column(ARRAY(String)))
    rating: float = 0.5

    created_date: datetime = Field(default_factory=lambda: datetime.now())
    modified_date: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": datetime.now},
    )
