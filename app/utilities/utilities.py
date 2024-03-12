import aiosqlite
import asyncio
from typing import Optional
from models.schemas import UserInDB, UserCreate


DATABASE_PATH = 'database.db'

async def initialize_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        query = """
        CREATE TABLE IF NOT EXISTS users(
            username VARCHAR(100),
            email VARCHAR(50),
            full_name VARCHAR(100),
            hashed_password VARCHAR(64)
        );
        """
        await db.executescript(query)
        await db.commit()
