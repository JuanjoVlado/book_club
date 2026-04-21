from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import auth_router

app = FastAPI()

# TODO: add routes
app.include_router(auth_router, prefix="/auth")

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


@app.get("/")
async def root():
    return {"message": "¡Hola, Mundo!"}


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy"}
