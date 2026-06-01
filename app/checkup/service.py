from fastapi import HTTPException

from .repository import checkup_repo
from .schemas import CheckupUpdate, CheckupCreate
from app.rents import rent_repo
from app.abstracts import AbstractService


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

