
from app.abstracts import AbstractRepository
from app.auth.schemas import LoginDto
from app.database import db
from app.users.schemas import UserCreate, UserUpdate
from app.users.user_model import User


class UserRepository(AbstractRepository[User, UserCreate, UserUpdate]):
    def __init__(self, db):
        self.collect =  db["users"]
        super().__init__(User, self.collect)

    async def find_for_logining(self, login_dto: LoginDto) -> User:
        return await self.collect.find_one({
            "$or": [
                {"email": login_dto.login},
                {"login": login_dto.login}
            ]
        })



user_repo = UserRepository(db)