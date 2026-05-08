import asyncio
import random
import string

from faker import Faker
from motor.motor_asyncio import AsyncIOMotorClient

from app.auth.schemas import UserPermissionsDto
from app.auto_models.service import AutoModelService
# from app.autos.repository import car_repo
from app.autos.schemas import CarCreate
# from app.brands import brand_repo
# from app.autos import Car, CarService
# from app.brands import Brand
# from app.auto_models.auto_model_model import AutoModel
from app.auto_models.schemas import AutoModelCreate, CarCategory
from app.autos import CarService
from app.brands.schemas import BrandCreate
from app.brands.service import BrandService
from app.rents.schemas import RentRequest
from app.rents.service import RentService
from app.users.schemas import UserCreate
from app.users.service import UserService

fake = Faker()


async def seed(iterations: int = 5):
    # 1. Подключаемся к локальной Монге
    client = AsyncIOMotorClient("mongodb://root:supersecretpassword@localhost:27017/?authSource=admin")

    await client.drop_database("rents_db")
    print("Database cleared")

    brand_serv = BrandService()
    model_serv = AutoModelService()
    car_serv = CarService()
    user_serv = UserService()
    remt_serv = RentService()

    for _ in range(iterations):
        user_dto = UserCreate(
            email=fake.unique.email(),
            login=fake.unique.user_name() + '_usr',
            password="string",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        new_user = await user_serv.create(user_dto)
        print(new_user)

        brand_dto = BrandCreate(
            name=fake.unique.company(),
            country=fake.country(),
            description=fake.sentence(nb_words=10)
        )

        new_brand = await brand_serv.create(brand_dto)
        print(new_brand)

        dto = AutoModelCreate(
            brand_id=new_brand.id,
            name=fake.word().capitalize() + random.choice([" X", " Series", " Pro", " GT"]),
            description="High quality vehicle with " + fake.bs(),
            category=random.choice(list(CarCategory))
        )
        new_model = await model_serv.create(dto)
        print(new_model)

        car_dto = CarCreate(
            model_id=new_model.id,
            # VIN должен быть ровно 17 символов (цифры + заглавные буквы)
            vin="".join(random.choices(string.ascii_uppercase + string.digits, k=17)),
            plate_number=fake.unique.bothify(text='?###??###').upper(),
            year=random.randint(2015, 2024),
            color=fake.color_name(),
            mileage=random.randint(0, 100000),
            price_per_day=float(random.randint(3000, 20000))
        )

        car = await car_serv.create(car_dto)
        print(car)


        rent_dto = RentRequest(
            car_id=car.id,
            driver=False,
            user_dock="".join(random.choices(string.ascii_uppercase + string.digits, k=8)),
            days_qty=random.randint(2, 60),
            start_date=fake.date_time_between(start_date='+1d', end_date='+1m')
        )

        user_payload = UserPermissionsDto(
            id=new_user.id,
            active=True,
            is_admin=False,
            is_manager=False,
        )
        new_rent = await remt_serv.create_rent(rent_dto, user_payload)
        print(new_rent)

    # Запуск


if __name__ == "__main__":
    asyncio.run(seed())
