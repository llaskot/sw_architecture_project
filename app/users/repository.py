from . import UserCreate
from .user_model import User
from ..auth.schemas import LoginDto


class UserRepository:
    def __init__(self, model):
        # Сохраняем модель внутри "себя"
        self.model = model

    async def save_user(self, user_dto: UserCreate) -> User:
        # create model
        new_user = self.model(**user_dto.model_dump())
        # MongoDB insert
        await new_user.insert()
        return new_user

    async def find_for_logining(self, login_dto: LoginDto) -> User:
        return await self.model.find_one({
            "$or": [
                {"email": login_dto.login},
                {"login": login_dto.login}
            ]
        })

    async def get_user_by_id(self, user_id) -> User | None:
        return await self.model.get(user_id)



user_repo = UserRepository(User)
