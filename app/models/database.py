import aiosqlite
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from models.schemas import UserInDB, UserCreate, User, CodeInDB, Code
import os
import random
from typing import Optional
from utilities.password_service import PasswordService

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
    
        
    async def get_user_code() -> Code:
        pass
    

    async def add_code_to_db(user: User, code: Code) -> bool | Code:
        user = await self.get_user_by_email(user_email)
        if user.ref_code is not None:
            return False
        
        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(
                "INSERT INTO codes (ref_code, user_id, exp_date) VALUES (?, ?, ?)",
                (code.ref_code, user.user_id, code.exp_date)
            )
            await db.commit()
        added_code = await self.get_user_code()
        return added_code