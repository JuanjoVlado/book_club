from fastapi import APIRouter, status
from app.schemas.user import UserAuthentication, UserRegister, UserLogin
from app.db.session import SessionDep

auth_router = APIRouter()

@auth_router.post("/register",
             tags=['auth'],
             response_model=UserAuthentication,
             status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegister, session: SessionDep):
    return {"message": "register"}

@auth_router.post("/login",
             tags=['auth'],
             response_model=UserAuthentication,
             status_code=status.HTTP_200_OK)
async def user_login(user_login: UserLogin, session: SessionDep):
    return {"message": "login"}

@auth_router.post("/logout",
             tags=['auth'],
             status_code=status.HTTP_200_OK)
             
async def user_logout():
    return {"message": "logout"}

