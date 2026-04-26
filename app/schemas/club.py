from sqlmodel import SQLModel

class ClubCreate(SQLModel):
    name: str
    description: str

class ClubUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    admin_id: int | None = None
