from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from app.core.security import get_current_user, require_admin
from app.db.session import SessionDep
from app.models.user import User, UserRole
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate

book_router = APIRouter()

@book_router.post("/", tags=["book"], status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate,
    session: SessionDep,
    require_admin: User = Depends(require_admin)
):
    
    statement = select(Book).where(Book.isbn == book_data.isbn)
    db_book = session.exec(statement).first()

    if db_book:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Book already exists"
        )
    
    book = Book(**book_data.model_dump())
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@book_router.get("/", tags=["book"], status_code=status.HTTP_200_OK, response_model=List[Book])
async def get_books(
    session: SessionDep,
    skip: int = 0,
    limit: int = 10
):
    statement = select(Book).offset(skip).limit(limit)
    books = session.exec(statement).all()
    return books

@book_router.get("/{id}", tags=["book"], status_code=status.HTTP_200_OK, response_model=Book)
async def get_book_by_id(
    id: int,
    session: SessionDep
):
    statement = select(Book).where(Book.id == id)
    book = session.exec(statement).first()

    if book:
        return book
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with id: {id} not found"
    )

@book_router.patch("/{id}", tags=["book"], status_code=status.HTTP_202_ACCEPTED)
async def update_book(
    id: int,
    book_data: BookUpdate,
    session: SessionDep,
    require_admin: User = Depends(require_admin)
):
    db_book = session.get(Book, id)

    if db_book:
        db_book.sqlmodel_update(book_data.model_dump(exclude_unset=True))
        session.add(db_book)
        session.commit()
        session.refresh(db_book)
        return db_book
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Invalid book id"
    )

@book_router.delete("/{id}", tags=["book"])
async def delete_book(
    id:int,
    session: SessionDep,
    require_admin: User = Depends(require_admin)
):
    db_book = session.get(Book, id)

    if db_book:
        session.delete(db_book)
        session.commit()
        return {"detail": "Book deleted"}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with id: {id} not found"
    )
