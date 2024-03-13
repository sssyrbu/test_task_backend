# Router for everything related to user accounts 
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.schemas import UserCreate, User, Token
from models.database import UserRepository
from typing import Optional
from utilities.password_service import PasswordService
from utilities.utilities import create_access_token, create_refresh_token 


user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Используйте существующие возможности сервиса."}},
)

password_service = PasswordService()

@user_router.post("/signup", response_model=User)
async def register_user(user_create: UserCreate) -> Optional[User]:
    user_repo = UserRepository(password_service)
    existing_user = await user_repo.get_user_by_email(user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с данной почтой уже существует."
        )

    new_user = await user_repo.create_user(user_create)
    message = f"Регистрация прошла успешно. Ваши данные: email='{new_user.email}'"
    return User(email=new_user.email, message=message)
    # return User(email=new_user.email)


@user_router.post('/login', summary="Войти в систему", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_repo = UserRepository(password_service)
    existing_user = await user_repo.get_user_by_email(form_data.username)
    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неправильная почта или пароль."
        )

    hashed_pass = existing_user.hashed_password
    if not password_service.verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неправильная почта или пароль."
        )
    
    return {
        "access_token": create_access_token(existing_user.email),
        "token_type": "bearer",
        "refresh_token": create_refresh_token(existing_user.email),
    }