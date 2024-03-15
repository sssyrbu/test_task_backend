import aiosqlite
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
            async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
                existing_user = await cursor.fetchone()

            if existing_user is not None:
                while existing_user[0] != user_id:
                    user_id = random.randint(10000, 99999)

            hashed_pass = self.password_service.get_password_hash(user_create.password)
            await db.execute(
                "INSERT INTO users (user_id, email, hashed_password) VALUES (?, ?, ?)",
                (user_id, user_create.email, hashed_pass)
            )
            await db.commit()
            new_user = await self.get_user_by_email(user_create.email)

            return new_user
    
        
    async def get_user_code(self, user: User) -> Optional[Code]:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute("SELECT * FROM codes WHERE user_id = ?", (user.user_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return Code(ref_code=row[0], exp_date=row[2])

        return None
    

    async def add_code_to_db(self, user: User, code: CodeInDB) -> bool | Code:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(
                "INSERT INTO codes (ref_code, exp_date, user_id) VALUES (?, ?, ?)",
                (code.ref_code, code.exp_date, user.user_id)
            )
            await db.commit()
        added_code = await self.get_user_code(user)

        return added_code
    

    async def delete_code_from_db(self, user: User) -> Optional[Code]:
        user_code = await self.get_user_code(user)
        if user_code is None:
            return None
        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute("DELETE FROM codes WHERE user_id = ?", (user.user_id,))
            await db.commit()

        return user_code