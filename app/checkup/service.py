from fastapi import HTTPException

from app.abstracts import AbstractService
from app.auto_models import auto_model_repo
from app.auto_models.auto_model_model import CarCategory
from app.auto_models.schemas import AutoModelCreate, AutoModelUpdate
from app.brands import brand_repo
from app.checkup.repository import checkup_repo
from app.checkup.schemas import CheckupUpdate, CheckupCreate
from app.rents.repository import rent_repo


class CheckupService(AbstractService[CheckupCreate, CheckupUpdate]):
    def __init__(self):
        super().__init__(checkup_repo)
        self.rent_repo = rent_repo

    async def check(self, data: CheckupCreate | CheckupUpdate):
        if not data.rent_id:
            return
        rent = await self.rent_repo.get_by_id(data.rent_id)
        if not rent or not rent.active:
            raise HTTPException(status_code=404, detail="Rent not found")

