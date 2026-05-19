from sqlmodel import SQLModel

class ChatMessageCreate(SQLModel):
    content: str
