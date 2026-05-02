import traceback

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.auth import auth_router
from app.api.v1.books import book_router
from app.api.v1.club import club_router
from app.api.v1.user_book import user_book_router
from app.api.v1.club_user import club_user_router
from app.api.v1.club_book import club_book_router

app = FastAPI()

# TODO: add routes
app.include_router(auth_router, prefix="/auth")
app.include_router(book_router, prefix="/books")
app.include_router(club_router, prefix="/clubs")
app.include_router(club_user_router, prefix="/clubs")
app.include_router(club_book_router, prefix="/clubs")
app.include_router(user_book_router, prefix="/users")

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "traceback": traceback.format_exc()}
    )

@app.get("/")
async def root():
    return {"message": "¡Hola, Mundo!"}


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy"}
