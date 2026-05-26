

# async def seed(iterations: int = 5):
#     # 1. Подключаемся к локальной Монге
#     # client = AsyncIOMotorClient("mongodb://root:supersecretpassword@localhost:27017/?authSource=admin")
#
#     # await client.drop_database("rents_db")
#
#     client = AsyncIOMotorClient(settings.database_url)
#     db_name = settings.mongo_db
#     await client.drop_database(db_name)
#     print("Database cleared")
#
#     brand_serv = BrandService()
#     model_serv = AutoModelService()
#     car_serv = CarService()
#     user_serv = UserService()
#     remt_serv = RentService()
#
#     for _ in range(iterations):
#         user_dto = UserCreate(
#             email=fake.unique.email(),
#             login=fake.unique.user_name() + '_usr',
#             password="Aa111111",
#             first_name=fake.first_name(),
#             last_name=fake.last_name(),
#         )
#         new_user = await user_serv.create(user_dto)
#         print(new_user)
#
#         brand_dto = BrandCreate(
#             name=fake.unique.company(),
#             country=fake.country(),
#             description=fake.sentence(nb_words=10)
#         )
#
#         new_brand = await brand_serv.create(brand_dto)
#         print(new_brand)
#
#         for i in range(10):
#             dto = AutoModelCreate(
#                 brand_id=new_brand.id,
#                 name=fake.word().capitalize() + random.choice([" X", " Series", " Pro", " GT"]),
#                 description="High quality vehicle with " + fake.bs(),
#                 category=random.choice(list(CarCategory))
#             )
#             new_model = await model_serv.create(dto)
#             print(new_model)
#
#
#             car_dto = CarCreate(
#                 model_id=new_model.id,
#                 # VIN должен быть ровно 17 символов (цифры + заглавные буквы)
#                 vin="".join(random.choices(string.ascii_uppercase + string.digits, k=17)),
#                 plate_number=fake.unique.bothify(text='?###??###').upper(),
#                 year=random.randint(2015, 2024),
#                 color=fake.color_name(),
#                 mileage=random.randint(0, 100000),
#                 price_per_day=float(random.randint(3000, 20000))
#             )
#
#             car = await car_serv.create(car_dto)
#             print(car)
#
#
#         rent_dto = RentRequest(
#             car_id=car.id,
#             driver=False,
#             user_dock="".join(random.choices(string.ascii_uppercase + string.digits, k=8)),
#             days_qty=random.randint(2, 60),
#             start_date=fake.date_time_between(start_date='+1d', end_date='+1m')
#         )
#
#         user_payload = UserPermissionsDto(
#             id=new_user.id,
#             active=True,
#             is_admin=False,
#             is_manager=False,
#         )
#         new_rent = await remt_serv.create_rent(rent_dto, user_payload)
#         print(new_rent)


async def seed(iterations: int = 5):
    client = AsyncIOMotorClient(settings.database_url)
    db_name = settings.mongo_db
    # Очищаем БД перед посевом
    await client.drop_database(db_name)
    print("Database cleared")

    brand_serv = BrandService()
    model_serv = AutoModelService()
    car_serv = CarService()
    user_serv = UserService()
    remt_serv = RentService()

    # Фиксированный каталог
    brands_catalog = [
        {"name": "Toyota", "country": "Japan", "models": ["Camry", "Corolla", "RAV4"]},
        {"name": "BMW", "country": "Germany", "models": ["3 Series", "5 Series", "X5"]},
        {"name": "Tesla", "country": "USA", "models": ["Model 3", "Model Y", "Model S"]},
        {"name": "Mercedes", "country": "Germany", "models": ["C-Class", "E-Class", "GLE"]},
        {"name": "Audi", "country": "Germany", "models": ["A4", "A6", "Q7"]}
    ]
    colors = ["Black", "White", "Silver", "Blue", "Red", "Gray"]

    print("Seeding Brands and Models...")
    created_models = []

    # === ЭТАП 1: Создаем бренды и модели ОДИН РАЗ (без дубликатов) ===
    for b_info in brands_catalog:
        brand_dto = BrandCreate(name=b_info["name"], country=b_info["country"], description="Official dealer")
        new_brand = await brand_serv.create(brand_dto)

        # Сразу создаем все модели для этого бренда
        for model_name in b_info["models"]:
            model_dto = AutoModelCreate(
                brand_id=new_brand.id,
                name=model_name,
                description=f"Reliable {b_info['name']} {model_name}",
                category=random.choice(list(CarCategory))  # Убедись, что CarCategory импортирован
            )
            new_model = await model_serv.create(model_dto)
            created_models.append(new_model)  # Сохраняем модели в список для дальнейшего использования

    print(f"Created {len(brands_catalog)} brands and {len(created_models)} models.")
    print("Seeding Users, Cars, and Rents...")

    # === ЭТАП 2: Генерируем пользователей и машины (iterations раз) ===
    for _ in range(iterations):
        # 1. Пользователь
        user_dto = UserCreate(
            email=fake.unique.email(),
            login=fake.unique.user_name(),
            password="Aa111111",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        new_user = await user_serv.create(user_dto)

        # 2. Создаем несколько машин (например, 3) для пула
        for _ in range(3):
            random_model = random.choice(created_models)  # Берем случайную уже созданную модель
            car_dto = CarCreate(
                model_id=random_model.id,
                vin="".join(random.choices(string.ascii_uppercase + string.digits, k=17)),
                plate_number=f"{random.randint(1000, 9999)} {random.choice(['AA', 'BK', 'KA', 'BC'])}",
                year=random.randint(2018, 2024),
                color=random.choice(colors),
                mileage=random.randint(5000, 90000),
                price_per_day=float(random.choice([1500, 2500, 3500, 5000, 7500]))
            )
            car = await car_serv.create(car_dto)

        # 3. Аренда (арендуем последнюю созданную в цикле машину)
        rent_dto = RentRequest(
            car_id=car.id,
            driver=False,
            user_dock="".join(random.choices(string.digits, k=9)),
            days_qty=random.randint(3, 14),
            start_date=fake.date_time_between(start_date='+1d', end_date='+10d')
        )
        user_payload = UserPermissionsDto(id=new_user.id, active=True, is_admin=False, is_manager=False)
        await remt_serv.create_rent(rent_dto, user_payload)

        print(f"Created: User {new_user.login} | Rent for car {car.plate_number}")








    # Запуск


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    val = input("1 - dev : 2 - stage : ")
    if val == '1':
        load_dotenv()
    else:
        # 1. Загружаем окружение СТРОГО до импортов из app
        load_dotenv("../staged/.env")
        os.environ["MONGO_HOST"] = "localhost"
        os.environ["MONGO_PORT"] = "27018"


    from app.core.config import settings
    import asyncio
    import random
    import string

    from faker import Faker
    from motor.motor_asyncio import AsyncIOMotorClient
    from app.auth.schemas import UserPermissionsDto
    from app.auto_models.service import AutoModelService
    from app.autos.schemas import CarCreate
    from app.auto_models.schemas import AutoModelCreate, CarCategory
    from app.autos import CarService
    from app.brands.schemas import BrandCreate
    from app.brands.service import BrandService
    from app.rents.schemas import RentRequest
    from app.rents.service import RentService
    from app.users.schemas import UserCreate
    from app.users.service import UserService

    fake = Faker()



    asyncio.run(seed())
