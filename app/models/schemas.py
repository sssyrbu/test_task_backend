from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    
    
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
    password: str


class UserInDB(User):
    hashed_password: str