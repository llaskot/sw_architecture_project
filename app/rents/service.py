from datetime import timedelta, datetime
from typing import Any

from bson import ObjectId
from fastapi import HTTPException


from .rent_model import Rent, RentStage
from .repository import rent_repo as rr, RentRepository
from .schemas import RentCreate, RentUpdate, RentRead, RentRequest, RentUpdateRequest, ChangeStage, UpdateStage
from app.users import UserPermissionsDto, user_repo as ur, UserRepository
from app.abstracts import AbstractService
from app.autos import car_repo as cr, Car, CarRepository, CarUpdate

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

        rent = RentCreate(
            **rent_req_dto.model_dump(),
            client_id=client_id,
            total_price=rent_req_dto.days_qty * car.price_per_day,
            end_date=rent_req_dto.start_date + timedelta(days=rent_req_dto.days_qty)
        )

        await self._check_availability(car.id, rent)
        rent = await self.repo.create(rent)
        return rent

    async def update_rent(self, rent_id: str, rent_req_dto: RentUpdateRequest, user_payload: UserPermissionsDto) -> Any:
        rent: RentRead = await self.repo.get_by_id(ObjectId(rent_id))
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

        # get info about actual car
        car_id = updated_rent.car_id or rent.car_id
        new_car: Car = await self.car_repo.get_by_id(car_id)
        if not new_car or not new_car.active:
            raise HTTPException(status_code=404, detail="Car not found")
        if not new_car.available:
            raise HTTPException(status_code=409, detail="Car is not available")

        # if important fields has not been changed
        if not (updated_rent.start_date or updated_rent.end_date or updated_rent.car_id):
            await self.repo.update(ObjectId(rent_id), updated_rent)
            return await self.repo.get_by_id(ObjectId(rent_id))

        updated_rent.total_price = (updated_rent.days_qty or rent.days_qty) * new_car.price_per_day
        updated_rent.start_date = (updated_rent.start_date or rent.start_date)
        updated_rent.end_date = ((updated_rent.start_date or rent.start_date)
                                 + timedelta(days=(updated_rent.days_qty or rent.days_qty)))

        await self._check_availability(car_id, updated_rent, rent.id)
        await self.repo.update(ObjectId(rent_id), updated_rent)
        return await self.repo.get_by_id(ObjectId(rent_id))

    async def _check_availability(self, checked_car_id, updated_rent: RentUpdate | RentCreate,
                                  rent_id: ObjectId = None):
        future_rents = await self.repo.get_by_car_id(checked_car_id)
        if not future_rents:
            return
        important_future_rents = []
        for future_rent in future_rents:
            if rent_id and rent_id == updated_rent.car_id:
                continue
            if future_rent.stage in ["ordered", "refused", "closed"]:
                continue
            important_future_rents.append(future_rent)
        self._check_is_overlapping(updated_rent.start_date, updated_rent.end_date, important_future_rents)

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
        return await self.repo.get_all_own(user.id, stage, sort_date, page, limit)

    async def get_all_admin_rents(self,
                                  stage,
                                  car_id: str,
                                  client_id: str,
                                  hide_inactive,
                                  sort_date,
                                  page: int,
                                  limit: int,
                                  user: UserPermissionsDto):
        inactive = hide_inactive if user.is_admin else True
        return await self.repo.get_all_admin(
            client_id=ObjectId(client_id) if client_id else None,
            car_id=ObjectId(car_id) if car_id else None,
            stage=stage,
            hide_inactive=inactive,
            sort_date=sort_date,
            page=page,
            limit=limit,
        )

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
        return res

    async def get_stages(self):
        return [stage.value for stage in RentStage]
