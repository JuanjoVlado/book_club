from enum import StrEnum
from typing import List
from sqlmodel import Relationship, SQLModel, Field
from pydantic import EmailStr
from datetime import date, datetime

from app.models.user_book import UserBook


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"

class UserStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"

class UserBase(SQLModel):
    name:str
    email: EmailStr
    date_of_birth: date
    status: UserStatus = UserStatus.ACTIVE
    created_date: datetime = Field(default_factory=lambda: datetime.now())
    role: UserRole = UserRole.USER

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(max_length=128)
    modified_date: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": datetime.now},
    )
    # clubs: Book   Club
    books: List["UserBook"] = Relationship()