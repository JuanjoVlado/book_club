from sqlmodel import SQLModel
from pydantic import EmailStr
from datetime import date

class UserLogin(SQLModel):
    email: EmailStr
    password: str

class UserRegister(UserLogin):
    name: str
    date_of_birth: date

class UserAuthentication(SQLModel):
    access_token: str
    token_type: str