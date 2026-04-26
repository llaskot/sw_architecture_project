from fastapi import HTTPException

from app.abstracts import AbstractService
from app.auto_models import auto_model_repo
from app.autos.repository import car_repo
from app.autos.schemas import CarCreate, CarUpdate, AllCarsResponse


class CarService(AbstractService[CarCreate, CarUpdate]):
    def __init__(self):
        super().__init__(car_repo)
        self.model_repo = auto_model_repo

    async def check(self, data: CarCreate | CarUpdate):
        if not data.model_id:
            return
        model = await self.model_repo.get_by_id(data.model_id)
        if not model or not model.active:
            raise HTTPException(status_code=404, detail="Car model not found")

    async def get_all_set(self, filters: dict) -> AllCarsResponse:
        return await self.repo.get_all_set(
            brand_ids=filters.get("brand_ids"),
            categories=filters.get("categories"),
            sort_price=filters.get("sort_price") if filters.get("sort_price") != "none" else None,
            sort_model=filters.get("sort_model") if filters.get("sort_model") != "none" else None,
            hide_inactive=filters.get("hide_inactive"),
            page=filters.get("page"),
            limit=filters.get("limit")
        )
