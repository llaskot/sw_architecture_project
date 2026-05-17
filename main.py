import asyncio
import logging
import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core import settings
from app.users.router import router as users_router
from app.auth.router import router as auth_router
from app.brands.router import router as brand_router
from app.files import  files_router
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
    os.makedirs(settings.upload_dir, exist_ok=True)
    print(f"Uploading directory is ready: {settings.upload_dir}")
    port = "8000"
    if "--port" in sys.argv:
        try:
            port = sys.argv[sys.argv.index("--port") + 1]
        except IndexError:
            pass
    url = "http://127.0.0.1:"
    print(f"\n🔗 API:     {url}{settings.expose_app_port or port}")
    print(f"📝 Swagger: {url}{settings.expose_app_port or port}/docs\n")

    if settings.expose_host:
        print(f"\n🔗Outside API:     http://{settings.expose_host}:{settings.expose_app_port}")
        print(f"📝Outside Swagger:   http://{settings.expose_host}:{settings.expose_app_port}/docs\n")
    yield
    worker_task.cancel()
    client.close()



app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173", # Стандартный порт Vite
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Разрешить все методы (POST, GET и т.д.)
    allow_headers=["*"], # Разрешить все заголовки
)


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

app.include_router(files_router)

app.mount(f"/{settings.upload_dir}", StaticFiles(directory=settings.upload_dir), name="static")
