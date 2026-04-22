from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from app.models.user import User
from app.schemas.user import UserAuthentication, UserRegister, UserLogin
from app.db.session import SessionDep
from app.core.security import hash_password, create_access_token

auth_router = APIRouter()

@auth_router.post("/register",
             tags=['auth'],
             status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegister, session: SessionDep):
    statement = select(User).where(User.email == user_data.email)
    exists = session.exec(statement).first()
    
    if exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"An user with this email already exists"
        )
    else:
        new_user = User(
            email=user_data.email,
            name=user_data.name,
            date_of_birth=user_data.date_of_birth,
            hashed_password=hash_password(user_data.password)
        )
        
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return {
            "message": "User created",
            "user_id": new_user.id,
            "access_token": create_access_token(new_user.email)
        }


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

