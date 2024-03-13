import aiosqlite
import asyncio
from models.schemas import UserInDB, UserCreate
from typing import Optional
from utilities.password_service import PasswordService

DATABASE_PATH = 'database.db'

class UserRepository:
    def __init__(self, password_service: PasswordService):
        self.db_path = DATABASE_PATH
        self.password_service = password_service


    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT * FROM users WHERE email = ?", (email,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return UserInDB(email=row[0], hashed_password=row[1])
        return None


    async def create_user(self, user_create: UserCreate) -> Optional[UserInDB]:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO users (email, hashed_password) VALUES (?, ?)",
                (user_create.email, self.password_service.get_password_hash(user_create.password))
            )
            await db.commit()
            new_user = await self.get_user_by_email(user_create.email)
            return new_user