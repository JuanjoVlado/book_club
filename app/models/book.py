from sqlmodel import SQLModel, Field
from enum import Enum

class BookStatus(str, Enum):
    READ="read"
    READING="reading"
    TO_READ="to_read"

class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author: str
    isbn: int = Field(default=None, unique=True)
    chapter_count: int
    page_count: int
    status: BookStatus = Field(default=BookStatus.TO_READ)
