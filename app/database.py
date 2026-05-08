# from dotenv import load_dotenv
#
# # 1. Загружаем переменные из файла .env в окружение (os.environ)
# load_dotenv()


import os
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings


# print(f"DEBUG: App is connecting to --> {settings.database_url}")
client = AsyncIOMotorClient(settings.database_url)
db = client[settings.mongo_db]

# Вся "грязная" работа с индексами здесь
async def setup_db():
    await db["brand"].create_index("name", unique=True)
    await db["auto_model"].create_index("name", unique=True)
    await db['cars'].create_index("plate_number", unique=True)
    await db['users'].create_index("login", unique=True)
    await db['users'].create_index("email", unique=True)
