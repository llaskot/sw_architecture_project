


import os

import bcrypt
from motor.motor_asyncio import AsyncIOMotorClient
from app.core import settings


client = AsyncIOMotorClient(settings.database_url)
db = client[settings.mongo_db]

# Вся работа с индексами здесь
async def setup_db():
    await db["brand"].create_index("name", unique=True)
    await db["auto_model"].create_index("name", unique=True)
    await db['cars'].create_index("plate_number", unique=True)
    await db['users'].create_index("login", unique=True)
    await db['users'].create_index("email", unique=True)

    # Проверка и создание первого админа
    if all([settings.first_admin_login, settings.first_admin_pass, settings.first_admin_mail]):
        exists = await db["users"].find_one({
            "$or": [
                {"login": settings.first_admin_login},
                {"email": settings.first_admin_mail}
            ]
        })

        if not exists:
            pwd_bytes = settings.first_admin_pass.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

            await db["users"].insert_one({
                "email": settings.first_admin_mail,
                "login": settings.first_admin_login,
                "password": hashed_password,
                "first_name": settings.first_admin_name or "Admin",
                "last_name": "Admin",
                "active": True,
                "is_admin": True,
                "is_manager": False
            })
            print("🚀 First admin user created via database setup")
        else:
            print("🚀 First admin already exists")