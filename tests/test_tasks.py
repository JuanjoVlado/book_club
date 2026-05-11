import random
import pytest
from requests import RequestException
import requests
import responses
from app.tasks import get_metadata_by_isbn
from celery.exceptions import MaxRetriesExceededError, Retry


@responses.activate
def test_get_isbn_success(test_client, books_created):
    book = random.choice(books_created["books"])

    responses.add(
        responses.GET,
        f"https://openlibrary.org/api/books?bibkeys=ISBN:{book["isbn"]}&format=json&jscmd=data",
        json={
            f"ISBN:{book["isbn"]}": {
                "url": "http://openlibrary.org/books/OL7353617M/Fantastic_Mr._Fox",
                "key": "/books/OL7353617M",
                "title": "Fantastic Mr. Fox",
                "authors": [
                    {
                        "url": "http://openlibrary.org/authors/OL34184A/Roald_Dahl",
                        "name": "Roald Dahl"
                    }
                ],
                "number_of_pages": 96,
                "identifiers": {
                    "goodreads": [
                        "1507552"
                    ],
                    "librarything": [
                        "6446"
                    ],
                    "isbn_10": [
                        "0140328726"
                    ],
                    "isbn_13": [
                        "9780140328721"
                    ],
                    "openlibrary": [
                        "OL7353617M"
                    ]
                },
                "publishers": [
                    {
                        "name": "Puffin"
                    }
                ],
                "publish_date": "October 1, 1988",
                "subjects": [
                    {
                        "name": "Animals",
                        "url": "https://openlibrary.org/subjects/animals"
                    },
                    {
                        "name": "Hunger",
                        "url": "https://openlibrary.org/subjects/hunger"
                    },
                    {
                        "name": "Open Library Staff Picks",
                        "url": "https://openlibrary.org/subjects/open_library_staff_picks"
                    },
                    {
                        "name": "Juvenile fiction",
                        "url": "https://openlibrary.org/subjects/juvenile_fiction"
                    },
                    {
                        "name": "Children's stories, English",
                        "url": "https://openlibrary.org/subjects/children's_stories,_english"
                    },
                    {
                        "name": "Foxes",
                        "url": "https://openlibrary.org/subjects/foxes"
                    },
                    {
                        "name": "Fiction",
                        "url": "https://openlibrary.org/subjects/fiction"
                    },
                    {
                        "name": "Zorros",
                        "url": "https://openlibrary.org/subjects/zorros"
                    },
                    {
                        "name": "Ficci\u00f3n juvenil",
                        "url": "https://openlibrary.org/subjects/ficci\u00f3n_juvenil"
                    },
                    {
                        "name": "Tunnels",
                        "url": "https://openlibrary.org/subjects/tunnels"
                    },
                    {
                        "name": "Interviews",
                        "url": "https://openlibrary.org/subjects/interviews"
                    },
                    {
                        "name": "Farmers",
                        "url": "https://openlibrary.org/subjects/farmers"
                    },
                    {
                        "name": "Children's stories",
                        "url": "https://openlibrary.org/subjects/children's_stories"
                    },
                    {
                        "name": "Rats",
                        "url": "https://openlibrary.org/subjects/rats"
                    },
                    {
                        "name": "Welsh Authors",
                        "url": "https://openlibrary.org/subjects/welsh_authors"
                    },
                    {
                        "name": "English Authors",
                        "url": "https://openlibrary.org/subjects/english_authors"
                    },
                    {
                        "name": "Thieves",
                        "url": "https://openlibrary.org/subjects/thieves"
                    },
                    {
                        "name": "Tricksters",
                        "url": "https://openlibrary.org/subjects/tricksters"
                    },
                    {
                        "name": "Badgers",
                        "url": "https://openlibrary.org/subjects/badgers"
                    },
                    {
                        "name": "Children's fiction",
                        "url": "https://openlibrary.org/subjects/children's_fiction"
                    },
                    {
                        "name": "Foxes, fiction",
                        "url": "https://openlibrary.org/subjects/foxes,_fiction"
                    },
                    {
                        "name": "Underground",
                        "url": "https://openlibrary.org/subjects/underground"
                    },
                    {
                        "name": "Renards",
                        "url": "https://openlibrary.org/subjects/renards"
                    },
                    {
                        "name": "Romans, nouvelles, etc. pour la jeunesse",
                        "url": "https://openlibrary.org/subjects/romans,_nouvelles,_etc._pour_la_jeunesse"
                    },
                    {
                        "name": "Children's literature",
                        "url": "https://openlibrary.org/subjects/children's_literature"
                    },
                    {
                        "name": "Plays",
                        "url": "https://openlibrary.org/subjects/plays"
                    },
                    {
                        "name": "Children's plays",
                        "url": "https://openlibrary.org/subjects/children's_plays"
                    },
                    {
                        "name": "Children's stories, Welsh",
                        "url": "https://openlibrary.org/subjects/children's_stories,_welsh"
                    },
                    {
                        "name": "Agriculteurs",
                        "url": "https://openlibrary.org/subjects/agriculteurs"
                    },
                    {
                        "name": "Fantasy fiction",
                        "url": "https://openlibrary.org/subjects/fantasy_fiction"
                    },
                    {
                        "name": "Children's plays, English",
                        "url": "https://openlibrary.org/subjects/children's_plays,_english"
                    }
                ],
                "subject_places": [
                    {
                        "name": "English countryside",
                        "url": "https://openlibrary.org/subjects/place:english_countryside"
                    }
                ],
                "subject_people": [
                    {
                        "name": "Bean",
                        "url": "https://openlibrary.org/subjects/person:bean"
                    },
                    {
                        "name": "Boggis",
                        "url": "https://openlibrary.org/subjects/person:boggis"
                    },
                    {
                        "name": "Bunce",
                        "url": "https://openlibrary.org/subjects/person:bunce"
                    },
                    {
                        "name": "Mr Fox",
                        "url": "https://openlibrary.org/subjects/person:mr_fox"
                    }
                ],
                "subject_times": [
                    {
                        "name": "20th Century",
                        "url": "https://openlibrary.org/subjects/time:20th_century"
                    }
                ],
                "excerpts": [
                    {
                        "text": "Down in the valley there were three farms.",
                        "comment": "",
                        "first_sentence": True
                    }
                ],
                "ebooks": [
                    {
                        "preview_url": "https://archive.org/details/fantasticmrfoxpu00roal",
                        "availability": "restricted",
                        "formats": {}
                    }
                ],
                "cover": {
                    "small": "https://covers.openlibrary.org/b/id/15152634-S.jpg",
                    "medium": "https://covers.openlibrary.org/b/id/15152634-M.jpg",
                    "large": "https://covers.openlibrary.org/b/id/15152634-L.jpg"
                }
            }
        },    
        status=200
    )
    
    get_metadata_by_isbn.apply(args=[book["id"], book["isbn"]])

    res = test_client.get(f"/books/{book["id"]}")
    assert res.status_code == 200
    data = res.json()
    assert data["isbn"] == book["isbn"]
    assert data["title"] == "Fantastic Mr. Fox"
    assert data["author"] == "Roald Dahl"

@responses.activate
def test_get_isbn_connection_error(test_client, books_created):
    book = random.choice(books_created["books"])

    responses.add(
        responses.GET,
        f"https://openlibrary.org/api/books?bibkeys=ISBN:{book["isbn"]}&format=json&jscmd=data",
        body=requests.exceptions.ConnectionError("Connection error")
    )

    with pytest.raises(Retry):
        get_metadata_by_isbn.apply(args=[book["id"], book["isbn"]])

@responses.activate
def test_get_isbn_book_not_found(test_client, books_created):
    max_book = max(books_created["books"], key=lambda book: book["id"])

    responses.add(
        responses.GET,
        f"https://openlibrary.org/api/books?bibkeys=ISBN:{max_book["isbn"]}&format=json&jscmd=data",
        status=200
    )

    result = get_metadata_by_isbn.apply(args=[max_book["id"]+1, max_book["isbn"]])
    assert result.result is None

@responses.activate
def test_get_isbn_invalid_isbn(test_client, books_created):
    book = random.choice(books_created["books"])
    isbn = book["isbn"] + "x_X"

    responses.add(
        responses.GET,
        f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data",
        status=200,
        json={}
    )

    result = get_metadata_by_isbn.apply(args=[book["id"], isbn])
    assert result.result is None
