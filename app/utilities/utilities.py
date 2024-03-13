import aiosqlite
import asyncio
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models.database import UserRepository
from models.schemas import User, UserInDB
from utilities.password_service import PasswordService
from typing import Union, Any


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
DATABASE_PATH = os.getenv("DATABASE_PATH")
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
password_service = PasswordService()


async def initialize_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        query = """
        CREATE TABLE IF NOT EXISTS users(
            email VARCHAR(100),
            hashed_password VARCHAR(64)
        );
        """
        await db.executescript(query)
        await db.commit()


def authenticate_user(fake_db, email: str, password: str):
    user = UserRepository(password_service)
    existing_user = user.get_user_by_email(email)
    if existing_user is None:
        return False
    if not password_service.verify_password(password, user.hashed_password):
        return False
    return existing_user


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt