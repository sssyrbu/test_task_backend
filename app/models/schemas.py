from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class User(BaseModel):
    user_id: int
    email: str
    
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserInDB(User):
    hashed_password: str


class Code(BaseModel):
    ref_code: str


class CodeInDB(Code):
    user_id: int
    exp_date: str 


class RefCodeCreate(BaseModel):
    expiration_in_minutes: int