from typing import List
from fastapi import APIRouter
from sqlmodel import select
from app.db.session import SessionDep
from app.models.book import Book
from app.schemas.book import BookResponse
from app.schemas.recommendation import RecommendationQuery
from app.tasks import generate_embedding

recommendation_router = APIRouter()

@recommendation_router.post("/recommendations/", tags=["books"],response_model=List[BookResponse])
def get_recommendations(session: SessionDep, query: RecommendationQuery):
    embedding = generate_embedding(query.query)
    statement = select(Book).order_by(Book.embedding.cosine_distance(embedding)).limit(5)
    db_books = session.exec(statement).all()
    return db_books
