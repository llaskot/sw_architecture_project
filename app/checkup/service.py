from fastapi import HTTPException

from .checkup_model import CheckupModel
from .repository import checkup_repo
from .schemas import CheckupUpdate, CheckupCreate, CheckupRead
from app.rents import rent_repo
from app.abstracts import AbstractService
from ..users import UserPermissionsDto


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

    async def get_checkup(self, check_id: str, user: UserPermissionsDto) -> CheckupRead:
        checkup = await self.get_by_id(check_id)
        if not checkup:
            raise HTTPException(status_code=404, detail="Checkup not found")
        if user.is_admin or user.is_manager or user.id == checkup.rent.client_id:
            return checkup
        raise HTTPException(status_code=403, detail="Checkup not admin")

    async def get_checkup_by_rent(self, rent_id: str, user: UserPermissionsDto) -> CheckupRead:
        checkup = await self.repo.get_checkup_by_rent(rent_id)
        if not checkup:
            raise HTTPException(status_code=404, detail="Checkup not found")
        if user.is_admin or user.is_manager or user.id == checkup.rent.client_id:
            return checkup
        raise HTTPException(status_code=403, detail="Checkup not admin")



