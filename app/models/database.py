import aiosqlite
import asyncio
from dotenv import load_dotenv
from models.schemas import UserInDB, UserCreate, User
import os
import random
from typing import Optional
from utilities.password_service import PasswordService

load_dotenv()

DATABASE_PATH = os.getenv("DATABASE_PATH")

class UserRepository:
    def __init__(self, password_service: PasswordService):
        self.db_path = DATABASE_PATH
        self.password_service = password_service


    async def get_user_by_email(self, email: str) -> Optional[User]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT * FROM users WHERE email = ?", (email,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return User(user_id=row[0], email=row[1])
        return None


    async def create_user(self, user_create: UserCreate) -> Optional[UserInDB]:
        async with aiosqlite.connect(self.db_path) as db:
            user_id = random.randint(0, 10000)
            hashed_pass = self.password_service.get_password_hash(user_create.password)
            await db.execute(
                "INSERT INTO users (id, email, hashed_password) VALUES (?, ?, ?)",
                (user_id, user_create.email, hashed_pass)
            )
            await db.commit()
            new_user = await self.get_user_by_email(user_create.email)
            return new_user