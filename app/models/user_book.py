from sqlmodel import Field, SQLModel
from app.models.book import BookStatus


class UserBook(SQLModel, table=True):
    user_id: int = Field(primary_key=True, foreign_key="user.id")
    book_id: int = Field(primary_key=True, foreign_key="book.id")
    status: BookStatus = BookStatus.PENDING
    progress: int = 0 # paginas leídas
    user_rating: float = 0
    notes: str = ""
