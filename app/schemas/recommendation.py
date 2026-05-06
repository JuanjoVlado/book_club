from sqlmodel import SQLModel


class RecommendationQuery(SQLModel):
    query: str
