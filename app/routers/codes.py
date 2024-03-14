# Router for everything related to referral code 
from datetime import datetime
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.schemas import User, RefCodeCreate
from models.database import UserRepository
from typing import Optional, Annotated
from utilities.deps import get_current_user
from utilities.password_service import PasswordService
from utilities.utilities import create_ref_code


from pydantic import BaseModel, Field
codes_router = APIRouter(
    prefix="/codes",
    tags=["codes"],
    responses={404: {"description": "Используйте существующие возможности сервиса."}},
)

password_service = PasswordService()
user_repo = UserRepository(password_service)


@codes_router.post('/create_code', summary='Сгенерировать реферальный код', response_model=Code)
async def create_code(create_exp: RefCodeCreate, current_user: Annotated[User, Depends(get_current_user)]):
    expiration_in_minutes = create_exp.expiration_in_minutes
    if expiration_in_minutes < 1: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Некорректное время истечения реферального кода."
        )
    created_code = Code(
        ref_code=create_ref_code(),
        user_id=current_user.user_id,
        exp_date=(datetime.now(timezone.utc) + timedelta(minutes=expiration_in_minutes)).isoformat()
    )



# @codes_router.post('/delete_code', summary='Удалить свой реферальный код', response_model=)
# async def delete_code(current_user: Annotated[User, Depends(get_current_user)]):
#     pass