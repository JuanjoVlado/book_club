from enum import StrEnum
from sqlmodel import Field, SQLModel
from app.models.club import ClubRole

class ClubUserStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"

class ClubUser(SQLModel, table=True):
    club_id: int = Field(primary_key=True, foreign_key="bookclub.id")
    user_id: int = Field(primary_key=True, foreign_key="user.id")
    user_status: ClubUserStatus = ClubUserStatus.ACTIVE
    user_role: ClubRole = ClubRole.USER
