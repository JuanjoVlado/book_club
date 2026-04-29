from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from app.core.security import get_current_user
from app.db.session import SessionDep
from app.models.book import Book
from app.models.user import User
from app.models.user_book import UserBook
from app.schemas.user_book import UserBookUpdate

user_book_router = APIRouter()

@user_book_router.post("/{user_id}/books/{book_id}", tags=["user"], status_code=status.HTTP_201_CREATED)
def create_user_book(
    user_id: int,
    book_id: int,
    session: SessionDep,
    user: User = Depends(get_current_user)
):
    if user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only add books to your own user account."
        )
    
    db_book = session.get(Book, book_id)

    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find book with id {book_id}"
        )
    
    existing = session.get(UserBook, (user_id, book_id))

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The book with id {book_id} is already associated with the user with id {user_id}"
        )

    userbook = UserBook(
        user_id=user_id,
        book_id=book_id
    )
    session.add(userbook)
    session.commit()
    session.refresh(userbook)
    return userbook
    

@user_book_router.get("/{user_id}/books", tags=["user"], response_model=List[UserBook])
def get_user_books(session: SessionDep, user_id: int):
    db_user = session.get(User, user_id)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    statement = select(UserBook).where(UserBook.user_id == user_id)
    user_books = session.exec(statement).all()
    return user_books

@user_book_router.get("/{user_id}/books/{book_id}", tags=["user"], response_model=UserBook)
def get_user_book_by_id(user_id: int, book_id: int, session: SessionDep):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    db_user_book = session.get(UserBook, (user_id, book_id))
    if not db_user_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found for User with id {user_id}"
        )
    
    return db_user_book

@user_book_router.patch("/{user_id}/books/{book_id}", tags=["user"], response_model=UserBook)
def update_user_book(
    user_id: int,
    book_id: int,
    session: SessionDep,
    user_book_data: UserBookUpdate,
    user: User = Depends(get_current_user)
):
    if user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to modify other user's books"
        )
    
    db_user_book = session.get(UserBook, (user_id, book_id))
    if not db_user_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find the combination of User with id {user_id} and Book with id {book_id}"
        )

    db_user_book.sqlmodel_update(user_book_data.model_dump(exclude_unset=True))
    session.add(db_user_book)
    session.commit()
    session.refresh(db_user_book)
    return db_user_book

@user_book_router.delete("/{user_id}/books/{book_id}", tags=["user"])
def delete_user_book(
    user_id: int,
    book_id: int,
    session: SessionDep,
    user: User = Depends(get_current_user)
):
    if user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to modify other user's books"
        )
    
    db_user_book = session.get(UserBook, (user_id, book_id))
    if not db_user_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find the combination of User with id {user_id} and Book with id {book_id}"
        )
    
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find the combination of User with id {user_id} and Book with id {book_id}"
        )
    
    session.delete(db_user_book)
    session.commit()
    return {"message": f"Book with id {book_id} removed from User with id {user_id}"}
