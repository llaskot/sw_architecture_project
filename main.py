from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.users.router import router as users_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    print("DB CONNECTED")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users_router)


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str | None = None):
#     """
#     this is description
#     """
#     return {"item_id": item_id, "q": q}