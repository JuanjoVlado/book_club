from sqlmodel import SQLModel

from app.models.club_user import ClubRole, ClubUserStatus

class ClubUserUpdate(SQLModel):
    user_status: ClubUserStatus = ClubUserStatus.ACTIVE
    user_role: ClubRole = ClubRole.USER
