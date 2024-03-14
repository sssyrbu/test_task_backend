from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

class User(BaseModel):
    email: str
    message: Optional[str] = None 
    
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserInDB(User):
    hashed_password: str