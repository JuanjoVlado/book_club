from celery import Celery
from app.core.config import settings

broker = "memory://" if settings.TESTING else settings.CELERY_REDIS_URL
backend = "cache+memory://" if settings.TESTING else settings.CELERY_REDIS_URL

app = Celery(
    "bookclubms",
    include=["app.tasks"],
    broker=broker,
    backend=backend
)

app.set_default()
app.set_current()

if settings.TESTING:
    app.conf.update(
        task_always_eager=True,
        task_eager_propagates=True,
    )
