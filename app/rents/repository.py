from datetime import datetime, timezone
from typing import Any

from bson import ObjectId

from app.abstracts import AbstractRepository
from app.database import db
from app.rents.rent_model import Rent
from app.rents.schemas import RentCreate, RentUpdate, RentRead


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


rent_repo = RentRepository(db)