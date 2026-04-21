from sqlmodel import SQLModel
from pydantic import EmailStr
from datetime import date


class UserRegister(SQLModel):
    name: str
    email: EmailStr
    password: str
    date_of_birth: date

class UserLogin(SQLModel):
    email: EmailStr
    password: str

class UserAuthentication(SQLModel):
    access_token: str
    token_type: str