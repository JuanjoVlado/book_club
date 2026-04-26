from sqlmodel import SQLModel
from pydantic import EmailStr
from datetime import date

from app.models.user import UserRole

class UserLogin(SQLModel):
    email: EmailStr
    password: str

class UserRegister(UserLogin):
    name: str
    date_of_birth: date

class UserAuthentication(SQLModel):
    access_token: str
    token_type: str

class UserUpdate(SQLModel):
    password: str | None = None
    name: str | None = None
    role: UserRole | None = None