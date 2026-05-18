from datetime import timedelta, datetime
from typing import Any

from bson import ObjectId
from fastapi import HTTPException
from watchfiles import awatch

from app.abstracts import AbstractService
from app.auth.schemas import UserPermissionsDto
from app.autos import car_repo as cr
from app.autos.repository import CarRepository
from app.autos.schemas import CarUpdate
from app.rents.rent_model import Rent, RentStage
from app.rents.repository import rent_repo as rr, RentRepository
from app.rents.schemas import RentCreate, RentUpdate, RentRead, RentRequest, RentUpdateRequest, ChangeStage, UpdateStage
from app.users.repository import user_repo as ur, UserRepository


class RentService(AbstractService[RentCreate, RentUpdate]):
    def __init__(self, rent_repo: RentRepository = rr, user_repo: UserRepository = ur, car_repo: CarRepository = cr):
        super().__init__(rent_repo)
        self.car_repo = car_repo  # Подключаем репо машин
        self.user_repo = user_repo  # Подключаем репо юзеров

    async def create_rent(self, rent_req_dto: RentRequest, user_payload: UserPermissionsDto) -> Rent:
        client_id = user_payload.id
        car = await self.car_repo.get_by_id(rent_req_dto.car_id)
        if not car or not car.active or not car.available or car.in_use:
            raise HTTPException(status_code=404, detail="Car not available")
        user = await self.user_repo.get_by_id(client_id)
        if not user or not user.active:
            raise HTTPException(status_code=404, detail="User not found")
        # car_upd_dto = CarUpdate(
        #     available=False
        # )
        rent = RentCreate(
            **rent_req_dto.model_dump(),
            client_id=client_id,
            total_price=rent_req_dto.days_qty * car.price_per_day,
            end_date=rent_req_dto.start_date + timedelta(days=rent_req_dto.days_qty)
        )
        future_rents = await self.repo.get_by_car_id(car.id)
        if future_rents:
            self._check_is_overlapping(rent.start_date, rent.end_date, future_rents)

        # await self.car_repo.update(rent_req_dto.car_id, car_upd_dto)
        rent = await self.repo.create(rent)
        return rent

    async def update_rent(self, rent_id: str, rent_req_dto: RentUpdateRequest, user_payload: UserPermissionsDto) -> Any:
        rent = await self.repo.get_by_id(ObjectId(rent_id))
        if not rent or not rent.active:
            raise HTTPException(status_code=404, detail="Rent not found")

        if not (user_payload.is_manager or user_payload.is_admin) and rent.client_id != user_payload.id:
            raise HTTPException(status_code=404, detail="Rent not found")

        if not (user_payload.is_manager or user_payload.is_admin) and rent.stage != "ordered":
            raise HTTPException(status_code=409, detail="Rent already confirmed")

        if user_payload.is_manager and rent.stage not in ("ordered", "refused", 'booked'):
            raise HTTPException(status_code=409, detail="Rent already payd")

        updated_rent = RentUpdate(
            **rent_req_dto.model_dump(),
        )
        if not (updated_rent.start_date or updated_rent.end_date or updated_rent.car_id):
            await self.repo.update(ObjectId(rent_id), updated_rent)
            return await self.repo.get_by_id(ObjectId(rent_id))
        car_id = updated_rent.car_id or rent.car_id
        new_car = await self.car_repo.get_by_id(car_id)
        future_rents = await self.repo.get_by_car_id(car_id)
        future_rents = [r for r in future_rents if r.id != rent.id]
        updated_rent.total_price = (updated_rent.days_qty or rent.days_qty) * new_car.price_per_day
        updated_rent.start_date = (updated_rent.start_date or rent.start_date)
        updated_rent.end_date = ((updated_rent.start_date or rent.start_date)
                                 + timedelta(days=(updated_rent.days_qty or rent.days_qty)))
        if future_rents:
            self._check_is_overlapping(updated_rent.start_date, updated_rent.end_date, future_rents)
        await self.repo.update(ObjectId(rent_id), updated_rent)
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

    async def get_rent(self, rent_id: str, user_payload: UserPermissionsDto):
        if user_payload.is_admin:
            hide_deleted = False
        else:
            hide_deleted = True
        res = await self.get_by_id(ObjectId(rent_id), hide_deleted)
        if not (user_payload.is_admin or user_payload.is_manager) and res.client_id != user_payload.id:
            raise HTTPException(status_code=404, detail="Rent not found")
        return res

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

    async def get_all_rents(self,
                            stage,
                            sort_date,
                            page: int,
                            limit: int,
                            user: UserPermissionsDto):
        # if user_payload.is_admin:
        #     hide_deleted = hide_inactive
        # else:
        #     hide_deleted = True
        # if user_payload.is_admin or user_payload.is_manager:
        #     return await self.get_all(hide_deleted)
        return await self.repo.get_all_own(user.id, stage, sort_date, page, limit)

    async def change_stage(self,
                           rent_id: str,
                           stage: RentStage,
                           body: ChangeStage,
                           user: UserPermissionsDto):
        rent: RentRead = await self.repo.get_by_id(ObjectId(rent_id))
        if not rent:
            raise HTTPException(status_code=404, detail="Rent not found")
        changes = UpdateStage(
            **body.model_dump(),
            updated_by=user.id,
            stage=stage
        )
        res = await self.repo.update(ObjectId(rent_id), changes)
        if not rent.car.available and stage != "ordered":
            car_changes = CarUpdate(
                available=True
            )
            await self.car_repo.update(ObjectId(rent.car_id), car_changes)
        return res
