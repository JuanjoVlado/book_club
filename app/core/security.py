import hashlib
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.core.config import settings
from jose import jwt
import bcrypt


crypt_context = CryptContext(schemes=["bcrypt"], truncate_error=False)

def hash_password(plain_password: str) -> str:
    sha = hashlib.sha256(plain_password.encode()).hexdigest()
    return bcrypt.hashpw(sha.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    sha = hashlib.sha256(plain_password.encode()).hexdigest()
    return bcrypt.checkpw(sha.encode(), hashed_password.encode())

def create_access_token(email: str) -> str:
    exp_timestamp = datetime.now() + timedelta(days=5)
    payload = {
        "sub": email,
        "exp": int(exp_timestamp.timestamp())
    }
    secret = settings.SECRET_KEY

    return jwt.encode(payload, secret, algorithm=settings.ALGORITHM)
