from fastapi import HTTPException

from app.abstracts import AbstractService
from app.auto_models import auto_model_repo
from app.autos.repository import car_repo
from app.autos.schemas import CarCreate, CarUpdate


class CarService(AbstractService[CarCreate, CarUpdate]):
    def __init__(self):
        super().__init__(car_repo)
        self.model_repo = auto_model_repo

    async def check(self, data: CarCreate | CarUpdate):
        model = await self.model_repo.get_by_id(data.model_id)
        if not model or not model.active:
            raise HTTPException(status_code=404, detail="Car model not found")