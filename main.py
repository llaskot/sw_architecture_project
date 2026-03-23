import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.database import init_db
from app.users.router import router as users_router
from app.auth.router import router as auth_router


logging.basicConfig(
    level=logging.ERROR,    # Логируем только ошибки и выше
    filename="app.error.log",     # Все "простыни" полетят в этот файл
    filemode="a",           # Дописывать в конец файла
    format="%(asctime)s - %(levelname)s - %(message)s"
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    print("DB CONNECTED")
    yield


app = FastAPI(lifespan=lifespan)


# 2. Error logging (Middleware)
@app.middleware("http")
async def error_logging_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logging.error(f"Error handling request {request.url.path}: {e}", exc_info=True)
        raise e from None
app.include_router(users_router)
app.include_router(auth_router)


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str | None = None):
#     """
#     this is description
#     """
#     return {"item_id": item_id, "q": q}