from models.database import UserRepository
from models.schemas import TokenPayload, User, UserInDB
from dotenv import load_dotenv
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os
from jose import jwt
from pydantic import ValidationError
from utilities.password_service import PasswordService

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
DATABASE_PATH = os.getenv("DATABASE_PATH")
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/users/login",
    scheme_name="JWT"
)

passw_service = PasswordService()
user_repo = UserRepository(passw_service)

async def get_current_user(token: str = Depends(reuseable_oauth)) -> User:
    # print(token)
    # a = jwt.decode(
    #         token, SECRET_KEY, algorithms=[ALGORITHM]
    #     )
    # print(a)
    # print(TokenPayload(exp=str(a["exp"]), sub=a["sub"]))
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(exp=str(payload["exp"]), sub=payload["sub"])
        
        if datetime.fromtimestamp(int(token_data.exp)) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Срок действия токена истек.",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет доступа к данному ресурсу.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await user_repo.get_user_by_email(token_data.sub) 
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Данный пользователь не найден",
        )

    return User(user_id=user.user_id, email=user.email)