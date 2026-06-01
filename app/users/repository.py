from bson import ObjectId

from app.abstracts import AbstractRepository
from app.database import db
from .schemas import UserCreate, UserUpdate, AllUsersResponse, UserResponseAdm, LoginDto
from .user_model import User


class UserRepository(AbstractRepository[User, UserCreate, UserUpdate]):
    def __init__(self, db):
        self.collect = db["users"]
        super().__init__(User, self.collect)

    async def find_for_logining(self, login_dto: LoginDto) -> User:
        return await self.collect.find_one({
            "active": True,
            "$or": [
                {"email": login_dto.login},
                {"login": login_dto.login},
            ]
        })

    async def change_password(self, user_id: str, new_pass: str):
        return await self.collect.update_one({"_id": ObjectId(user_id)}, {"$set": {"password": new_pass}})


    async def get_all_search(self, search: str, hide_inactive:bool, page: int, limit: int):
        print(hide_inactive)
        query = {}
        if hide_inactive:
            query["active"]= hide_inactive
        if search:
            # Регулярка: "i" означает case-insensitive (игнорировать регистр букв)
            search_regex = {"$regex": search, "$options": "i"}
            query["$or"] = [
                {"email": search_regex},
                {"first_name": search_regex},
                {"last_name": search_regex}
            ]
        skip = (page - 1) * limit

        pipeline = [
            {"$match": query},  # фильтруем базу
            {
                "$facet": {
                    "total_count": [{"$count": "count"}],  # Считаем совпадения
                    "data": [
                        {"$skip": skip},  # Пропускаем
                        {"$limit": limit}  # Ограничиваем
                    ]
                }
            }
        ]

        cursor = self.collect.aggregate(pipeline)
        res = await cursor.to_list(length=None)

        total = res[0]["total_count"][0]["count"] if res[0]["total_count"] else 0
        return AllUsersResponse(
            total=total,
            page=page,
            limit=limit,
            items=[UserResponseAdm.model_validate(r) for r in res[0]["data"]]
        )


user_repo = UserRepository(db)
