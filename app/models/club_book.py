from sqlmodel import Field, SQLModel
from app.models.book import BookStatus

class ClubBook(SQLModel, table=True):
    club_id: int = Field(primary_key=True, foreign_key="bookclub.id")
    book_id: int = Field(primary_key=True, foreign_key="book.id")
    status: BookStatus = BookStatus.PENDING
    club_rate: float = 0
    