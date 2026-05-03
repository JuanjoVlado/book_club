import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from sqlmodel import Session
from app.db.session import engine
from app.models.book import Book
from app.schemas.book import BookUpdate

OPEN_LIBRARY_URL = "https://openlibrary.org/api/books"

logger = get_task_logger(__name__)

@shared_task(bind=True)
def get_metadata_by_isbn(self, book_id: int, isbn: str):
    with Session(engine) as session:
        db_book = session.get(Book, book_id)
        if not db_book:
            logger.warning(f"Book with id {book_id} not found in the Database")
            return

        try:
            response = requests.get(
                f"{OPEN_LIBRARY_URL}?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
            )

            ol_data = response.json()

            if not ol_data:
                logger.warning(f"Open Library responded with an empty dict for ISBN: {isbn}")
                return
            
            ol_data = ol_data[f"ISBN:{isbn}"]
            authors = [author["name"] for author in ol_data["authors"]] if ol_data.get("authors") else None
            publishers = [publisher["name"] for publisher in ol_data["publishers"]] if ol_data.get("publishers") else None
            subjects = [subject["name"] for subject in ol_data["subjects"]] if ol_data.get("subjects") else None

            update_book = BookUpdate(
                title=ol_data.get("title"),
                author=",".join(authors) if authors else None,
                editorial= ",".join(publishers) if publishers else None,
                page_count=ol_data.get("number_of_pages"),
                genre=subjects if subjects else None
            )

            db_book.sqlmodel_update(update_book.model_dump(mode="json", exclude_unset=True))
            session.add(db_book)
            session.commit()
            logger.info(f"Book with id {book_id} updated with Open Library data for ISBN:{isbn}")
        
        except Exception as exc:
            logger.warning(f"Request failed. Retrying: {exc}")
            self.retry(exc=exc, countdown=5, max_retries=3)
