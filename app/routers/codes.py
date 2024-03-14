# Router for everything related to referral code 
# Router for everything related to user accounts 
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.schemas import UserCreate, User, UserInDB
from models.database import UserRepository
from typing import Optional, Annotated
from utilities.deps import get_current_user
from utilities.password_service import PasswordService


codes_router = APIRouter(
    prefix="/codes",
    tags=["codes"],
    responses={404: {"description": "Используйте существующие возможности сервиса."}},
)

password_service = PasswordService()
user_repo = UserRepository(password_service)

@codes_router.post('/create_code', summary='Сгенерировать реферальный код', response_model=User)
async def create_code(expiration_in_minutes: Annotated[int, Depends(get_current_user)]):
    pass


@codes_router.post('/delete_code', summary='Удалить свой реферальный код', response_model=User)
async def delete_code(current_user: Annotated[User, Depends(get_current_active_user)]):
    pass