import os
from typing import Final

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.auto_models import AutoModel
from app.autos import Car
from app.brands import Brand
from app.rents import Rent
from app.users import User

# 1. Загружаем переменные из файла .env в окружение (os.environ)
load_dotenv()


async def init_db():

    USER: Final = os.getenv("MONGO_USER")
    PASSWORD: Final = os.getenv("MONGO_PASSWORD")
    PORT: Final = os.getenv("MONGO_PORT")

    # mongodb://root:password@localhost:27017
    database_url = f"mongodb://{USER}:{PASSWORD}@localhost:{PORT}"

    client = AsyncIOMotorClient(database_url)

    await init_beanie(
        # database=cast(AsyncDatabase, cast(object, client.rents_db)),
        database=client.rents_db,
        document_models=[User, AutoModel, Brand, Car, Rent]
    )