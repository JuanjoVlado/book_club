from typing import List
from sqlmodel import SQLModel


class BookCreate(SQLModel):
    title: str
    author: str
    editorial: str
    description: str
    page_count: int
    isbn: str
    genre: List[str]

class BookUpdate(SQLModel):
    title: str | None = None
    author: str | None = None
    editorial: str | None = None
    description: str | None = None
    page_count: int | None = None
    isbn: str | None = None
    genre: List[str] | None = None
