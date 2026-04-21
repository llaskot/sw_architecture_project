from bson import ObjectId
from fastapi import HTTPException

from app.abstracts import AbstractService
from app.autos import car_repo
from app.autos.schemas import CarUpdate
from app.rents.rent_model import Rent
from app.rents.repository import rent_repo
from app.rents.schemas import RentCreate, RentUpdate, RentRead, RentRequest
from app.users.repository import user_repo


class RentService(AbstractService[RentCreate, RentUpdate]):
    def __init__(self):
        super().__init__(rent_repo)
        self.car_repo = car_repo  # Подключаем репо машин
        self.user_repo = user_repo  # Подключаем репо юзеров

    async def create(self, rent_req_dto: RentRequest) -> Rent:

        car = await self.car_repo.get_by_id(rent_req_dto.car_id)
        if not car or not car.active or not car.available or car.in_use:
            raise HTTPException(status_code=404, detail="Car not available")
        user = await self.user_repo.get_by_id(rent_req_dto.client_id)
        if not user or not user.active:
            raise HTTPException(status_code=404, detail="User not found")
        car_upd_dto = CarUpdate(
            available=False,
        )
        await self.car_repo.update(rent_req_dto.car_id, car_upd_dto)
        data = rent_req_dto.model_dump()
        print(type(data["car_id"]))
        rent = RentCreate(
            **rent_req_dto.model_dump(),
            total_price=rent_req_dto.days_qty * car.price_per_day
        )
        print(type(rent.car_id))
        rent.car_id = ObjectId(rent.car_id)
        print(type(rent.car_id))
        rent = await rent_repo.create(rent)
        return rent



    # async def check(self, data: RentCreate | RentUpdate):
    #     car = await self.car_repo.get_by_id(data.car_id)
    #     if not car or not car.active:
    #         raise HTTPException(status_code=404, detail="Car not found")
