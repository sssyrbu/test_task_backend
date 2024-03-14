import aiosqlite
import asyncio
from dotenv import load_dotenv
from models.schemas import UserInDB, UserCreate, User
import os
import random
from typing import Optional
from utilities.password_service import PasswordService
from utilities.utilities import create_ref_code

load_dotenv()

DATABASE_PATH = os.getenv("DATABASE_PATH")

class UserRepository:
    def __init__(self, password_service: PasswordService):
        self.password_service = password_service


    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute("SELECT * FROM users WHERE email = ?", (email,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return UserInDB(user_id=row[0], email=row[1], hashed_password=row[2])
        return None
    

    async def create_user(self, user_create: UserCreate) -> Optional[User]:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            user_id = random.randint(10000, 99999)
            hashed_pass = self.password_service.get_password_hash(user_create.password)
            await db.execute(
                "INSERT INTO users (id, email, hashed_password) VALUES (?, ?, ?)",
                (user_id, user_create.email, hashed_pass)
            )
            await db.commit()
            new_user = await self.get_user_by_email(user_create.email)
            return new_user
        

    async def add_code_to_db(user_email: str) -> bool:
        user = await self.get_user_by_email(user_email)
        if user.ref_code is not None:
            return False
        
        ref_code = create_ref_code()
        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(
                "UPDATE users SET ref_code = ? WHERE email = ?",
                (ref_code, user_email)
            )
            await db.commit()
        return True