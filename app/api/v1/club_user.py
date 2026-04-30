from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from app.core.security import require_club_admin
from app.db.session import SessionDep
from app.models.club import BookClub
from app.models.club_user import ClubUser
from app.models.user import User
from app.schemas.club_user import ClubUserUpdate

club_user_router = APIRouter()

### CREATE
@club_user_router.post(
    "/{club_id}/users/{user_id}",
    tags=["club"],
    status_code=status.HTTP_201_CREATED,
    response_model=ClubUser
)
def create_club_user(
    session: SessionDep,
    club_id: int,
    user_id: int,
    club_admin: User = Depends(require_club_admin)
):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found."
        )
    
    db_club_user = session.get(ClubUser, (club_id, user_id))
    if db_club_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with id {user_id} is already a member of Club with id {club_id}"
        )

    club_user = ClubUser(club_id=club_id, user_id=user_id)
    session.add(club_user)
    session.commit()
    session.refresh(club_user)
    return club_user

### GET
@club_user_router.get(
    "/{club_id}/users",
    tags=["club"],
    response_model=List[ClubUser]
)
def get_club_users(session: SessionDep, club_id: int):
    db_club = session.get(BookClub, club_id)
    if not db_club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book Club with id {club_id} not found"
        )
    
    statement = select(ClubUser).where(ClubUser.club_id == club_id)
    club_users = session.exec(statement).all()

    return club_users

### GET BY ID
@club_user_router.get(
    "/{club_id}/users/{user_id}",
    tags=["club"],
    response_model=ClubUser
)
def get_club_user_by(session: SessionDep, club_id: int, user_id: int):
    db_club_user = session.get(ClubUser, (club_id, user_id))
    if not db_club_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found in Book Club with id {club_id}"
        )
    
    return db_club_user

### UPDATE
@club_user_router.patch(
    "/{club_id}/users/{user_id}",
    tags=["club"],
    response_model=ClubUser,
    status_code=status.HTTP_202_ACCEPTED
)
def update_club_user(
    session: SessionDep,
    club_id: int,
    user_id: int,
    club_user_data: ClubUserUpdate,
    club_admin: User = Depends(require_club_admin)
):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    db_club_user = session.get(ClubUser, (club_id, user_id))
    if not db_club_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found in Book Club with id {club_id}"
        )
    
    db_club_user.sqlmodel_update(club_user_data.model_dump(exclude_unset=True))
    session.add(db_club_user)
    session.commit()
    session.refresh(db_club_user)
    return db_club_user

### DELETE
@club_user_router.delete("/{club_id}/users/{user_id}", tags=["club"])
def delete_club_user(
    session: SessionDep,
    club_id: int,
    user_id: int,
    club_admin: User = Depends(require_club_admin)
):
    db_club_user = session.get(ClubUser, (club_id, user_id))
    if not db_club_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found in Book Club with id {club_id}"
        )
    
    session.delete(db_club_user)
    session.commit()
    return {"message": f"User with id {user_id} removed from Book Club with id {club_id}"}
