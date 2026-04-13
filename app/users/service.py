import bcrypt

from app.abstracts import AbstractService
from app.users.repository import user_repo
from app.users.schemas import UserCreate, UserUpdate


class UserService(AbstractService[UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(user_repo)

    async def create(self, data: UserCreate):
        password = self.get_password_hash(data.password)
        data.password = password
        return await self.repo.create(data)

    def get_password_hash(self, password: str) -> str:
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(pwd_bytes, salt)
        return hashed_password.decode('utf-8')