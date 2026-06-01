from fastapi import HTTPException

from .repository import auto_model_repo
from .auto_model_model import CarCategory
from .schemas import AutoModelCreate, AutoModelUpdate
from app.brands import brand_repo
from app.abstracts import AbstractService


class AutoModelService(AbstractService[AutoModelCreate, AutoModelUpdate]):
    def __init__(self):
        super().__init__(auto_model_repo)
        self.brand_repo = brand_repo

    async def check(self, data: AutoModelCreate | AutoModelUpdate):
        if not data.brand_id:
            return
        brand = await self.brand_repo.get_by_id(data.brand_id)
        if not brand or not brand.active:
            raise HTTPException(status_code=404, detail="Brand not found")

    async def get_categories(self):
        return [category.value for category in CarCategory]