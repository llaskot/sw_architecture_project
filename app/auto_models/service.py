from fastapi import HTTPException

from app.abstracts import AbstractService
from app.auto_models import auto_model_repo
from app.auto_models.schemas import AutoModelCreate, AutoModelUpdate
from app.brands import brand_repo


class AutoModelService(AbstractService[AutoModelCreate, AutoModelUpdate]):
    def __init__(self):
        super().__init__(auto_model_repo)
        self.brand_repo = brand_repo

    async def check(self, data: AutoModelCreate | AutoModelUpdate):
        brand = await self.brand_repo.get_by_id(data.brand_id)
        if not brand or not brand.active:
            raise HTTPException(status_code=404, detail="Brand not found")