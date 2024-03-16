from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[str]
    exp: Optional[str]


class User(BaseModel):
    user_id: int
    email: str
    
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    signup_ref_code: Optional[str]


class UserInDB(User):
    hashed_password: str
    referrer_id: Optional[int] = None


class Code(BaseModel):
    ref_code: str
    exp_date: str 
    

class CodeInDB(Code):
    user_id: int


class RefCodeCreate(BaseModel):
    expiration_in_minutes: int

