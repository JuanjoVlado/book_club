from datetime import datetime
from enum import StrEnum
from typing import List
from sqlmodel import Field, Relationship, SQLModel
from app.models.user import User


class ChatRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"

class Chat(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    messages: List["ChatMessage"] | None = Relationship(back_populates="chat")
        
    created_date: datetime = Field(default_factory=lambda: datetime.now())
    modified_date: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": datetime.now},
    )

class ChatMessage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    role: ChatRole
    content: str
    chat_id: int = Field(foreign_key="chat.id")
    chat: Chat = Relationship(back_populates="messages")

    created_date: datetime = Field(default_factory=lambda: datetime.now())
