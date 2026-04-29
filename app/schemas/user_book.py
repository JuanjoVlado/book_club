
from sqlmodel import SQLModel
from app.models.book import BookStatus

class UserBookUpdate(SQLModel):
    status: BookStatus | None = None
    progress: int | None = None
    user_rating: float | None = None
    notes: str | None = None
