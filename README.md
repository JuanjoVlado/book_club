# Description
### Book Club Management System

This project provides an API to manage a book club. It allows to create and modify Users, Books and Clubs. Each User can create a list of books they have read, are reading or would like to read in the future, add notes to the book and assign a personal rating to it.

The API also allows to create a BookClub, manage the Users that conform the club and create a list of books for the club to read.

The API also includes a recommendation feature. You can provide a description of the type of book you would like to read and receive a list of books that match your requirements.

# Stack
### Database
- PostgreSQL with pgvector
- alembic for migrations

### Backend
- Python with FastAPI
- SentenceTransformers for semantic queries
- Celery and Redis for background tasks

### Testing
- pytest for testing

# ENV Variables
### Authentication
- **SECRET_KEY** (required): For JWT authentication. 
- **ANTHROPIC_API_KEY** (required): The API uses Anthropic service to improve the queries for book recommendations.
- **HF_TOKEN** (optional): The API uses public Hugging Face services to create the embeddings for the books when created. Having a valid token improves the rate limit.

### DB Connection
- DB_HOST
- DB_PORT
- DB_USERNAME
- DB_PASSWORD
- DB_NAME

Alternatively, you can provide a DATABASE_URL connection string directly instead of the individual DB variables.

# How To Use
### Setup
Create a new folder for the project and clone the repository
```bash
git clone git@github.com:JuanjoVlado/book_club.git
```
Create a new SECRET_KEY
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
Copy the new key to .env and also add the Database credentials to the .env.

### Docker
Build the images with
```bash
docker compose build
```
Run the containers
```bash
docker compose up -d
```

### Migrations
Migrations run from the container:
```bash
docker compose exec api .venv/bin/alembic upgrade head
```

Once running, you can access to the interactive documentation at http://localhost:8000/docs
