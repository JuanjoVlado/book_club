from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from app.core.security import get_current_user, require_club_admin
from app.db.session import SessionDep
from app.models.club import BookClub
from app.models.user import User
from app.schemas.club import ClubCreate, ClubUpdate

club_router = APIRouter()

@club_router.get("/", tags=["club"], status_code=status.HTTP_200_OK, response_model=List[BookClub])
def list_clubs(session: SessionDep, skip: int = 0, limit:int = 10):
    statement = select(BookClub).offset(skip).limit(limit)
    clubs = session.exec(statement).all()

    return clubs

@club_router.get("/{club_id}", tags=["club"], status_code=status.HTTP_200_OK, response_model=BookClub)
def get_club_by_id(club_id: int, session: SessionDep):
    club = session.get(BookClub, club_id)

    if club:
        return club
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Club not found"
    )

@club_router.post("/", tags=["club"], status_code=status.HTTP_201_CREATED, response_model=BookClub)
def create_club(
    club_data: ClubCreate,
    session: SessionDep,
    user: User = Depends(get_current_user),
):
    statement = select(BookClub).where(BookClub.name == club_data.name)
    db_club = session.exec(statement).first()

    if db_club:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"There is a Club named {club_data.name} already. Choose a different name for your club."
        )

    new_club = BookClub(**club_data.model_dump(), admin_id=user.id)


    session.add(new_club)
    session.commit()
    session.refresh(new_club)
    return new_club

@club_router.patch("/{club_id}", tags=["club"], status_code=status.HTTP_202_ACCEPTED, response_model=BookClub)
def update_club(session: SessionDep, club_id: int, club_data: ClubUpdate, club_admin = Depends(require_club_admin)):
    club = club_admin["club"]

    club.sqlmodel_update(club_data.model_dump(exclude_unset=True))
    session.add(club)
    session.commit()
    session.refresh(club)
    return club

@club_router.delete("/{club_id}", tags=["club"])
def delete_club(session: SessionDep, club_id: int, club_admin = Depends(require_club_admin)):
    club = club_admin["club"]

    session.delete(club)
    session.commit()
    return {"detail": f"Club {club.name} deleted."}
