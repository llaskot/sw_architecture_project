import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.users.router import router as users_router
from app.auth.router import router as auth_router
from app.brands.router import router as brand_router
from app.database import client, setup_db
from app.auto_models import auto_models_router
from app.autos import car_router
from app.rents.router import router as rent_router
from app.checkup import checkup_router
from app.mailer.consumer import dispatcher, consumer


logging.basicConfig(
    level=logging.ERROR,    # Логируем только ошибки и выше
    filename="app.error.log",     # Все "простыни" полетят в этот файл
    filemode="a",           # Дописывать в конец файла
    format="%(asctime)s - %(levelname)s - %(message)s"
)



@asynccontextmanager
async def lifespan(_: FastAPI):
    await setup_db()
    print("🚀 Database is ready")
    worker_task = asyncio.create_task(consumer())
    print("LOG: Consumer started")
    yield
    worker_task.cancel()
    client.close()



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
#
app.include_router(brand_router)
#
app.include_router(auto_models_router)
app.include_router(car_router)
#
app.include_router(rent_router)

app.include_router(checkup_router)

