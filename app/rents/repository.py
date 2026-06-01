from datetime import datetime, timezone
from typing import Any

from bson import ObjectId

from .rent_model import Rent, RentStage
from .schemas import RentCreate, RentUpdate, RentRead,  AllOwnRentsResponse
from app.abstracts import AbstractRepository
from app.database import db

class RentRepository(AbstractRepository[Rent, RentCreate, RentUpdate]):
    def __init__(self, db):
        super().__init__(Rent, db["rents"])
        self.response_model = RentRead
        self.read_pipeline = [
            # 1. Достаем саму МАШИНУ (Car) из коллекции 'cars'
            {
                "$lookup": {
                    "from": "users",  # Имя коллекции с "железом"
                    "localField": "client_id",  # Поле в коллекции Rents
                    "foreignField": "_id",
                    "as": "client"
                }
            },
            {
                "$unwind": {
                    "path": "$client",
                    "preserveNullAndEmptyArrays": True
                }
            },

            {
                "$lookup": {
                    "from": "cars",  # Имя коллекции с "железом"
                    "localField": "car_id",  # Поле в коллекции Rents
                    "foreignField": "_id",
                    "as": "car"
                }
            },
            {
                "$lookup": {
                    "from": "cars",
                    "localField": "car_id",
                    "foreignField": "_id",
                    "as": "car"
                }
            },
            {
                "$unwind": {
                    "path": "$car",
                    "preserveNullAndEmptyArrays": True
                }
            },

            # 2. Внутри машины достаем МОДЕЛЬ (AutoModel)
            {
                "$lookup": {
                    "from": "auto_model",
                    "localField": "car.model_id",  # Поле уже внутри объекта car
                    "foreignField": "_id",
                    "as": "car.model"
                }
            },
            {
                "$unwind": {
                    "path": "$car.model",
                    "preserveNullAndEmptyArrays": True
                }
            },

            # 3. Внутри модели достаем БРЕНД (Brand)
            {
                "$lookup": {
                    "from": "brand",
                    "localField": "car.model.brand_id",  # Идем еще глубже в дерево
                    "foreignField": "_id",
                    "as": "car.model.brand"
                }
            },
            {
                "$unwind": {
                    "path": "$car.model.brand",
                    "preserveNullAndEmptyArrays": True
                }
            },

            # 4. Очистка: если машины нет, выкидываем пустые ветки
            {
                "$addFields": {
                    "car": {
                        "$cond": [
                            {"$ifNull": ["$car._id", False]},
                            "$car",
                            "$$REMOVE"
                        ]
                    }
                }
            }
        ]

    async def get_by_car_id(self, car_id: ObjectId) -> Any:
        now = datetime.now(timezone.utc)
        match_stage = {"$match": {
            "car_id": car_id,
            "active": True,
            "end_date": {"$gt": now}
        }}
        cursor = self.collection.find(match_stage["$match"])
        documents = await cursor.to_list(length=None)
        if not documents or len(documents) == 0: return None
        return [self.model.model_validate(doc) for doc in documents]

    def get_set_pipeline(self,
                         client_id: ObjectId,
                         stage: list[RentStage] = None,
                         sort_date: datetime = None,
                         page: int = 1,
                         limit: int = 2,
                         hide_inactive: bool = True,
                         car_id: ObjectId = None,
                         ):
        pipeline: list[dict] = self.read_pipeline.copy()

        # 1. Фильтрация (Match)
        match_filter = {}
        if hide_inactive:
            match_filter["active"] = True
        if car_id:
            match_filter["car_id"] = car_id
        if client_id:
            match_filter["client_id"] = client_id
        if stage:
            match_filter["stage"] = {"$in": stage}
        print("match_filter", match_filter)

        pipeline.append({"$match": match_filter})

        sort_dict = {}
        if sort_date:
            sort_dict["updated_at"] = -1 if sort_date == "desc" else 1
        sort_dict["_id"] = 1
        pipeline.append({"$sort": sort_dict})

        # ПАГИНАЦИЯ
        skip = (page - 1) * limit
        pipeline.append({
            "$facet": {
                "total_count": [{"$count": "count"}],  # Считаем общее кол-во
                "data": [  # Забираем кусок данных
                    {"$skip": skip},
                    {"$limit": limit}
                ]
            }
        })
        return pipeline

    async def get_all_own(self,
                          client_id: ObjectId,
                          stage: list[RentStage],
                          # hide_inactive,
                          sort_date,
                          page,
                          limit
                          ) -> AllOwnRentsResponse:

        full_pipeline: list[dict] = self.get_set_pipeline(
            client_id,
            stage,
            sort_date,
            page,
            limit
        )
        cursor = self.collection.aggregate(full_pipeline)
        res = await cursor.to_list(length=None)
        total = res[0]["total_count"][0]["count"] if res[0]["total_count"] else 0
        return AllOwnRentsResponse(
            total=total,
            page=page,
            limit=limit,
            items=[self.response_model.model_validate(doc) for doc in res[0]["data"]]
        )

    async def get_all_admin(self,
                            client_id: ObjectId,
                            car_id: ObjectId,
                            stage,
                            hide_inactive,
                            sort_date,
                            page: int,
                            limit: int,
                            ) -> AllOwnRentsResponse:

        full_pipeline: list[dict] = self.get_set_pipeline(
            client_id,
            stage,
            sort_date,
            page,
            limit,
            hide_inactive,
            car_id
        )
        cursor = self.collection.aggregate(full_pipeline)
        res = await cursor.to_list(length=None)
        total = res[0]["total_count"][0]["count"] if res[0]["total_count"] else 0
        return AllOwnRentsResponse(
            total=total,
            page=page,
            limit=limit,
            items=[self.response_model.model_validate(doc) for doc in res[0]["data"]]
        )




rent_repo = RentRepository(db)
