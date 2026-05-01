from sqlmodel import Field, SQLModel
from app.models.book import BookStatus

class ClubBookUpdate(SQLModel):
    status: BookStatus = BookStatus.PENDING
    club_rate: float = Field(default=0, ge=0.0, le=1.0)
