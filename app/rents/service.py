from datetime import timedelta, datetime
from typing import Any

from bson import ObjectId
from fastapi import HTTPException

from app.abstracts import AbstractService
from app.autos import car_repo
from app.autos.schemas import CarUpdate
from app.rents.rent_model import Rent
from app.rents.repository import rent_repo
from app.rents.schemas import RentCreate, RentUpdate, RentRead, RentRequest, RentUpdateRequest
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
            available=False
        )
        rent = RentCreate(
            **rent_req_dto.model_dump(),
            total_price=rent_req_dto.days_qty * car.price_per_day,
            end_date=rent_req_dto.start_date + timedelta(days=rent_req_dto.days_qty)
        )
        future_rents = await self.repo.get_by_car_id(car.id)
        if future_rents:
            self._check_is_overlapping(rent.start_date, rent.end_date, future_rents)

        await self.car_repo.update(rent_req_dto.car_id, car_upd_dto)
        rent = await rent_repo.create(rent)
        return rent

    async def update(self, rent_id: str, rent_req_dto: RentUpdateRequest, hide_inactive: bool = None) -> Any:
        rent = await self.repo.get_by_id(ObjectId(rent_id))
        if not rent or not rent.active:
            raise HTTPException(status_code=404, detail="Rent not found")
        updated_rent = RentUpdate(
            **rent_req_dto.model_dump(),
        )
        if updated_rent.start_date or updated_rent.days_qty:
            updated_rent.end_date = ((rent_req_dto.start_date or rent.start_date) +
                                     timedelta(days=(rent_req_dto.days_qty or rent.days_qty)))
        new_car = None
        old_car_id = rent.car_id
        if rent_req_dto.car_id and rent.car_id != rent_req_dto.car_id:
            new_car = await self.car_repo.get_by_id(rent_req_dto.car_id)
            if not new_car:
                raise HTTPException(status_code=404, detail="Car not found")

            future_rents = await self.repo.get_by_car_id(new_car.id)
            if future_rents:
                self._check_is_overlapping(
                    updated_rent.start_date or rent.start_date,
                    updated_rent.end_date or rent.end_date,
                    future_rents)

            updated_rent.car_id = new_car.id
        if new_car and (not new_car.active or not new_car.available or new_car.in_use):
            raise HTTPException(status_code=404, detail="Car not available")

        if updated_rent.days_qty or new_car:
            updated_rent.total_price = ((updated_rent.days_qty or rent.days_qty) *
                                        (new_car.price_per_day if new_car else rent.car.price_per_day))
        if new_car:
            car_upd_dto = CarUpdate(available=True, )
            await self.car_repo.update(old_car_id, car_upd_dto)
            car_upd_dto = CarUpdate(available=False, )
            await self.car_repo.update(new_car.id, car_upd_dto)
        # Чтобы exclude_unset в репозитории их увидел как "не тронутые"
        updated_rent.__pydantic_fields_set__ = {
            name for name in updated_rent.__dict__
            if updated_rent.__dict__[name] is not None
        }
        await self.repo.update(ObjectId(rent_id), updated_rent)
        await self.repo.get_by_id(ObjectId(rent_id))
        return await self.repo.get_by_id(ObjectId(rent_id))

    async def delete_rent(self, rent_id: str) -> Any:
        rent = await self.repo.get_by_id(ObjectId(rent_id))
        if not rent:
            raise HTTPException(status_code=404, detail="Rent not found")
        car_upd_dto = CarUpdate(available=True)
        await self.car_repo.update(rent.car_id, car_upd_dto)
        success = await self.repo.delete(ObjectId(rent_id))
        if not success:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"success": True}

    def _check_is_overlapping(self, required_start: datetime, required_end: datetime, bookings: list[Rent]):
        for rent in bookings:
            start = rent.start_date - timedelta(days=1)
            end = rent.end_date + timedelta(days=1)
            if self._is_overlapping(required_start.replace(tzinfo=None), required_end.replace(tzinfo=None), start, end):
                raise HTTPException(
                    status_code=409,
                    detail={
                        "message": f"The car is already booked from {start} to {end}",
                    })

    def _is_overlapping(self, start1: datetime, end1: datetime, start2: datetime, end2: datetime) -> bool:
        return start1 <= end2 and start2 <= end1
