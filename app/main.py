from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import codes, users
from utilities.utilities import initialize_db
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users.user_router)
app.include_router(codes.codes_router)

    
@app.get("/")
async def root():
    return {"message": "Главная страница. Перейдите в /docs для UI документации"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)