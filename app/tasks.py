import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from sentence_transformers import SentenceTransformer
from sqlmodel import Session
from app.db.session import engine
from app.models.book import Book
from app.schemas.book import BookUpdate
from app.core.config import settings
from requests.exceptions import RequestException

OPEN_LIBRARY_URL = "https://openlibrary.org/api/books"

logger = get_task_logger(__name__)

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", token=settings.HT_TOKEN)
    return _model

@shared_task(bind=True)
def get_metadata_by_isbn(self, book_id: int, isbn: str):
    try:
        with Session(engine) as session:
            db_book = session.get(Book, book_id)
            if not db_book:
                logger.warning(f"Book with id {book_id} not found in the Database")
                return

            response = requests.get(
                f"{OPEN_LIBRARY_URL}?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
            )

            ol_data = response.json()

            if not ol_data:
                logger.warning(f"Open Library responded with an empty dict for ISBN: {isbn}")
                return
            logger.info("### ", ol_data)
            ol_data = ol_data[f"ISBN:{isbn}"]
            authors = [author["name"] for author in ol_data["authors"]] if ol_data.get("authors") else None
            publishers = [publisher["name"] for publisher in ol_data["publishers"]] if ol_data.get("publishers") else None
            subjects = [subject["name"] for subject in ol_data["subjects"]] if ol_data.get("subjects") else None

            update_book = BookUpdate(
                title=ol_data.get("title"),
                author=",".join(authors) if authors else None,
                editorial= ",".join(publishers) if publishers else None,
                page_count=ol_data.get("number_of_pages") | db_book.page_count,
                genre=subjects if subjects else None
            )

            db_book.sqlmodel_update(update_book.model_dump(mode="json", exclude_unset=True))
            session.add(db_book)
            session.commit()
            logger.info(f"Book with id {book_id} updated with Open Library data for ISBN:{isbn}")
   
    except RequestException as re:
        logger.warning(f"Request failed. Retrying: {re}")
        self.retry(exc=re, countdown=5, max_retries=3)

    except Exception as exc:
        logger.warning(f"Unexpected error: {exc}")

def create_embedding(source_text: str):
    model = get_model()
    return model.encode([source_text])[0].tolist()

@shared_task(bind=True)
def generate_embedding(self, book_id: int, source_text: str | None = None):
    try:
        with Session(engine) as session:
            db_book = session.get(Book, book_id)
            if not db_book:
                logger.warning(f"Could not find Book with id {book_id}.")
                return
            
            if not source_text:
                source_text = ",".join(db_book.genre) if db_book.genre else None
                if not source_text:
                    logger.warning(f"Unable to generate embeddings for Book with id {book_id}. Not source found for embedding.")
                    return

            db_book.embedding=create_embedding(source_text)
            session.add(db_book)
            session.commit()

    except RequestException as re:
        logger.warning(f"Request failed. Retrying: {re}")
        self.retry(exc=re, countdown=5, max_retries=3)

    except Exception as exc:
        logger.warning(f"Unexpected error: {exc}")
