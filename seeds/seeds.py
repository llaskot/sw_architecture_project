import asyncio
import random
import string

from faker import Faker
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.auto_models import auto_model_repo
from app.autos.schemas import CarCreate
from app.brands import brand_repo
from app.autos import Car, CarService
from app.brands import Brand
from app.auto_models.auto_model_model import AutoModel
from app.auto_models.schemas import AutoModelCreate, CarCategory
from app.autos import CarService
from app.brands.schemas import BrandCreate
from app.rents import rent_repo
from app.rents.schemas import RentCreate
from app.rents.tent_model import Rent
from app.users import user_repo, UserCreate, User

fake = Faker()

async def seed(iterations: int = 5):
    # 1. Подключаемся к локальной Монге
    client = AsyncIOMotorClient("mongodb://root:supersecretpassword@localhost:27017/?authSource=admin")
    await init_beanie(database=client.rents_db, document_models=[Brand, AutoModel, Car, User, Rent])

    model_rep = auto_model_repo
    brand_rep = brand_repo
    user_rep = user_repo
    rent_rep = rent_repo


    for _ in range(iterations):
        user_dto = UserCreate(
            email=fake.unique.email(),
            login=fake.unique.user_name(),
            password="$2b$12$GxiGn5xuZgymuIQxTzqEZOkl8kdBn99lcGH2PAFTU8bzNxHwpn4fu",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        new_user = await user_rep.save_user(user_dto)
        print(new_user)

        brand_dto = BrandCreate(
            name=fake.unique.company(),
            country=fake.country(),
            description=fake.sentence(nb_words=10)
        )

        new_brand = await brand_rep.save_brand(brand_dto)
        print(new_brand)


        dto = AutoModelCreate(
            brand_id=new_brand.id,
            name=fake.word().capitalize() + random.choice([" X", " Series", " Pro", " GT"]),
            description="High quality vehicle with " + fake.bs(),
            category=random.choice(list(CarCategory))
        )
        new_model = await model_rep.save_auto_model(dto)
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

        car = await CarService.create_car(car_dto)
        print(car)

        rent_dto = RentCreate(
            client = new_user.id,
            car = car.id,
            user_dock = "".join(random.choices(string.ascii_uppercase + string.digits, k=8)),
            days_qty = random.randint(2, 60),
        )
        new_rent = await rent_repo.save_rent(rent_dto)
        print(new_rent)



# Запуск
if __name__ == "__main__":
    asyncio.run(seed())
