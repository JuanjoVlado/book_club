import requests
from app.celery_app import app
from celery.utils.log import get_task_logger

OPEN_LIBRARY_URL = "https://openlibrary.org/api/books"

logger = get_task_logger(__name__)

@app.task(bind=True)
def get_metadata_by_isbn(self, isbn: str):
    try:
        response = requests.get(
            f"{OPEN_LIBRARY_URL}?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
        )

        return response.json()
    
    except Exception as exc:
        logger.warning(f"Request failed. Retrying: {exc}")
        self.retry(exc=exc, countdown=5, max_retries=3)
