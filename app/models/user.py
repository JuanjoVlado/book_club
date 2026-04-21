from enum import StrEnum
from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from datetime import date, datetime


class UserStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: EmailStr = Field(unique=True)
    hashed_password: str
    date_of_birth: date
    status: UserStatus = UserStatus.ACTIVE
    created_date: datetime = Field(default_factory=lambda: datetime.now())
    modified_date: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": datetime.now},
    )
    # clubs: BookClub
    # books: Book
