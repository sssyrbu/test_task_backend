import aiosqlite
import asyncio
from typing import Optional
from models.schemas import UserInDB, UserCreate

DATABASE_PATH = 'database.db'

class UserRepository:
    def __init__(self):
        self.db_path = DATABASE_PATH


    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT * FROM users WHERE email = ?", (email,)) as cursor:
                row = await cursor.fetchone()
                print(row)
                if row:
                    return UserInDB(username=row[0], email=row[1], full_name=row[2], hashed_password=row[3])
        return None


    async def create_user(self, user_create: UserCreate) -> UserInDB:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO users (username, email, full_name, hashed_password) VALUES (?, ?, ?, ?)",
                (user_create.username, user_create.email, user_create.full_name, user_create.password)
            )
            await db.commit()
            new_user = await self.get_user_by_email(user_create.email)
            return new_user