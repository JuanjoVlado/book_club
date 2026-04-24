from datetime import datetime
from enum import StrEnum
from sqlmodel import Field, SQLModel

class ClubRole(StrEnum):
    USER = "user"
    ADMIN = "administrator"
    MOD = "moderator" 

class BookClub(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    description: str
    #books: List[Book]
    #members: List[User]
    admin_id: int = Field(default=None, foreign_key="user.id")

    created_date: datetime = Field(default_factory=lambda: datetime.now())
    updated_date: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": datetime.now}    
    )
