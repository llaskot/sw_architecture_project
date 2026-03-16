from pymongo.errors import DuplicateKeyError

from app.users.schemas import User, UserCreate
from fastapi import HTTPException


class UserService:
    @staticmethod
    async def register_new_user(user_data: UserCreate):

        new_user = User(**user_data.model_dump()) # create model

        try:
            await new_user.insert()
            return new_user

        except DuplicateKeyError as e:
            details = e.details.get("keyValue", {})
            key, value = next(iter(details.items()), ("unknown field", "unknown value"))

            raise HTTPException(
                status_code=400,
                detail=f"Already exists: {key}: {value}"
            )