import os
from typing import Final

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
# from beanie import init_beanie

# from app.auto_models import AutoModel
# from app.autos import Car
from app.brands import Brand
# from app.rents import Rent
# from app.users import User

# 1. Загружаем переменные из файла .env в окружение (os.environ)
load_dotenv()


# async def init_db():
#
#     USER: Final = os.getenv("MONGO_USER")
#     PASSWORD: Final = os.getenv("MONGO_PASSWORD")
#     PORT: Final = os.getenv("MONGO_PORT")
#
#     # mongodb://root:password@localhost:27017
#     database_url = f"mongodb://{USER}:{PASSWORD}@localhost:{PORT}"
#
#     client = AsyncIOMotorClient(database_url)
#     db_r = client.rents_db
#     await db_r["brand"].create_index("name", unique=True)
#     return db_r
#
# db = init_db()

import os
from motor.motor_asyncio import AsyncIOMotorClient

_url = f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@localhost:27017"
client = AsyncIOMotorClient(_url)
db = client.rents_db

# Вся "грязная" работа с индексами здесь
async def setup_db():
    await db["brand"].create_index("name", unique=True)
    await db["auto_model"].create_index("name", unique=True)
    await db['cars'].create_index("plate_number", unique=True)