# Router for everything related to user accounts 
from fastapi import APIRouter, Depends, HTTPException
from models.schemas import UserCreate, User
from models.database import UserRepository


user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Используйте существующие возможности сервиса."}},
)


@user_router.post("/register", response_model=User)
async def register_user(user_create: UserCreate):
    user_repo = UserRepository()
    existing_user = await user_repo.get_user_by_email(user_create.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с данной почтой уже существует.")

    # Similarly, create a new user using the instance method
    new_user = await user_repo.create_user(user_create)

    return User(**new_user.dict())