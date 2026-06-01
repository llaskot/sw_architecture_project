import bcrypt

from app.abstracts import AbstractService
from app.users.repository import user_repo
from .schemas import UserCreate, UserUpdate, UserPermissionsDto


class UserService(AbstractService[UserCreate, UserUpdate]):
    def __init__(self, repo=user_repo):
        super().__init__(repo)

    async def create(self, data: UserCreate):
        password = self.get_password_hash(data.password)
        data.password = password
        return await self.repo.create(data)

    def get_password_hash(self, password: str) -> str:
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(pwd_bytes, salt)
        return hashed_password.decode('utf-8')

    async def get_all_search(self,
                             search: str,
                             hide_inactive: bool,
                             page: int,
                             limit: int,
                             user: UserPermissionsDto):
        inactive = hide_inactive if user.is_admin else True
        return await self.repo.get_all_search(search, inactive, page, limit)

