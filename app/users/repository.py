from .user_model import User
from app.users.schemas import UserCreate  # Твоя DTO для регистрации


class UserRepository:
    @staticmethod
    async def save_user(user_dto: UserCreate) -> User:
            # create model
            new_user = User(**user_dto.model_dump())

            # MongoDB insert
            await new_user.insert()
            return new_user

# Создаем единственный экземпляр репозитория (Вариант 3)
user_repo = UserRepository()