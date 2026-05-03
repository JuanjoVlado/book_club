from celery import Celery
from app.core.config import settings

app = Celery(
    "bookclubms",
    include=["app.tasks"],
    broker=settings.CELERY_REDIS_URL,
    backend=settings.CELERY_REDIS_URL
)
