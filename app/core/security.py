import hashlib
import bcrypt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from sqlmodel import select
from app.core.config import settings
from jose import JWTError, jwt
from app.db.session import SessionDep
from app.models.user import User
from fastapi.security import OAuth2PasswordBearer


crypt_context = CryptContext(schemes=["bcrypt"], truncate_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

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

def get_current_user(session: SessionDep, access_token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
        statement = select(User).where(User.email == payload["sub"])
        db_user = session.exec(statement).first()
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid credentials"
        )
    
    if db_user:
        return db_user
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid credentials"
    )
