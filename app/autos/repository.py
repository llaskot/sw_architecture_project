
from app.abstracts import AbstractRepository
from app.autos import Car
from app.autos.schemas import CarCreate, CarUpdate, CarRead
from app.database import db


class CarRepository(AbstractRepository[Car, CarCreate, CarUpdate]):
    def __init__(self):
        super().__init__(Car, db['cars'])
        self.response_model = CarRead
        self.read_pipeline = [
            # 1. Достаем модель
            {
                "$lookup": {
                    "from": "auto_model",
                    "localField": "model_id",
                    "foreignField": "_id",
                    "as": "model"
                }
            },
            # 2. Разворачиваем
            {
                "$unwind": {
                    "path": "$model",
                    "preserveNullAndEmptyArrays": True
                }
            },
            # 3. Джоиним бренд (БЕЗ удаления модели перед этим!)
            {
                "$lookup": {
                    "from": "brand",
                    "localField": "model.brand_id",
                    "foreignField": "_id",
                    "as": "model.brand"
                }
            },
            {
                "$unwind": {
                    "path": "$model.brand",
                    "preserveNullAndEmptyArrays": True
                }
            },
            # 4. ФИНАЛЬНАЯ ОЧИСТКА (делаем один раз в самом конце)
            {
                "$addFields": {
                    "model": {
                        "$cond": [
                            {"$ifNull": ["$model._id", False]},
                            "$model",
                            "$$REMOVE"  # Если нет ID модели, удаляем всё дерево model целиком
                        ]
                    }
                }
            }
        ]
car_repo = CarRepository()