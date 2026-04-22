from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.core.config import settings
from jose import jwt

crypt_context = CryptContext(schemes=["bcrypt"])

def hash_password(plain_password: str) -> str:
    return crypt_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return crypt_context.verify(plain_password, hashed_password)

def create_access_token(email: str) -> str:
    exp_timestamp = datetime.now() + timedelta(days=5)
    payload = {
        "sub": email,
        "exp": int(exp_timestamp.timestamp())
    }
    secret = settings.SECRET_KEY

    return jwt.encode(payload, secret, algorithm=settings.ALGORITHM)