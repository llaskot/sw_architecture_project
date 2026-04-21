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



        # self.read_pipeline = [
        #     # Достаем car
        #     {
        #         "$lookup": {
        #             "from": "car",
        #             "localField": "car_id",
        #             "foreignField": "_id",
        #             "as": "car"
        #         }
        #     },
        #     {
        #         "$unwind": {
        #             "path": "$car",
        #             "preserveNullAndEmptyArrays": True
        #         }
        #     },
        #
        #     # 1. Достаем модель
        #     {
        #         "$lookup": {
        #             "from": "auto_model",
        #             "localField": "car.model_id",
        #             "foreignField": "_id",
        #             "as": "car.model"
        #         }
        #     },
        #     # 2. Разворачиваем
        #     {
        #         "$unwind": {
        #             "path": "$car.model",
        #             "preserveNullAndEmptyArrays": True
        #         }
        #     },
        #     # 3. Джоиним бренд (БЕЗ удаления модели перед этим!)
        #     {
        #         "$lookup": {
        #             "from": "brand",
        #             "localField": "car.model.brand_id",
        #             "foreignField": "_id",
        #             "as": "car.model.brand"
        #         }
        #     },
        #     {
        #         "$unwind": {
        #             "path": "$car.model.brand",
        #             "preserveNullAndEmptyArrays": True
        #         }
        #     },
        #     # 4. ФИНАЛЬНАЯ ОЧИСТКА (делаем один раз в самом конце)
        #     {
        #         "$addFields": {
        #             "car": {
        #                 "$cond": [
        #                     {"$ifNull": ["$car._id", False]},
        #                     "$car",
        #                     "$$REMOVE"
        #                 ]
        #             }
        #         }
        #     }
        # ]


rent_repo = RentRepository(db)