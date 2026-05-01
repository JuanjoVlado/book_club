from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from app.core.security import require_club_admin
from app.db.session import SessionDep
from app.models.book import Book
from app.models.club_book import ClubBook
from app.models.user import User
from app.schemas.club_book import ClubBookUpdate

club_book_router = APIRouter()

### POST
@club_book_router.post(
        "/{club_id}/books/{book_id}",
        tags=["club-book"],
        status_code=status.HTTP_201_CREATED,
        response_model=ClubBook
)
def create_club_book(
    session: SessionDep,
    club_id: int,
    book_id: int,
    club_admin: User = Depends(require_club_admin)
):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    
    db_club_book = session.get(ClubBook, (club_id, book_id))
    if db_club_book:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The Book with id {book_id} is already on Club with id {club_id}"
        )
    
    new_club_book = ClubBook(club_id=club_id, book_id=book_id)
    session.add(new_club_book)
    session.commit()
    session.refresh(new_club_book)
    return new_club_book

### GET
@club_book_router.get(
        "/{club_id}/books", tags=["club-book"],
        response_model=List[ClubBook]
    )
def get_all_club_books(
    session: SessionDep,
    club_id: int
):
    statement = select(ClubBook).where(ClubBook.club_id == club_id)
    club_books = session.exec(statement).all()
    return club_books

@club_book_router.get(
        "/{club_id}/books/{book_id}",
        tags=["club-book"],
        response_model=ClubBook
    )
def get_club_book_by_id(
    session: SessionDep,
    club_id: int,
    book_id: int,
):
    db_club_book = session.get(ClubBook, (club_id, book_id))
    if not db_club_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found in Club with id {club_id}"
        )
    
    return db_club_book

### PATCH
@club_book_router.patch(
        "/{club_id}/books/{book_id}",
        tags=["club-book"],
        response_model=ClubBook,
        status_code=status.HTTP_202_ACCEPTED
    )
def update_club_book(
    session: SessionDep,
    club_id: int,
    book_id: int,
    data: ClubBookUpdate,
    club_admin: User = Depends(require_club_admin)
):
    db_club_book = session.get(ClubBook, (club_id, book_id))
    if not db_club_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found in Club with id {club_id}"
        )
    
    db_club_book.sqlmodel_update(data.model_dump(mode="json", exclude_unset=True))
    session.add(db_club_book)
    session.commit()
    session.refresh(db_club_book)
    return db_club_book

### DELETE
@club_book_router.delete("/{club_id}/books/{book_id}", tags=["club-book"])
def delete_club_book(
    session: SessionDep,
    club_id: int,
    book_id: int,
    club_admin: User = Depends(require_club_admin)
):
    db_club_book = session.get(ClubBook, (club_id, book_id))
    if not db_club_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found in Club with id {club_id}"
        )
    
    session.delete(db_club_book)
    session.commit()
    return {"message": f"Book with id {book_id} removed from Club with id {club_id}"}
