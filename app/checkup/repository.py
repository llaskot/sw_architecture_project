# from app.auto_models import AutoModel
from app.abstracts.abstract_repository import AbstractRepository
from app.auto_models.auto_model_model import AutoModel
from app.auto_models.schemas import AutoModelUpdate, AutoModelCreate, AutoModelRead
from app.checkup.checkup_model import CheckupModel
from app.checkup.schemas import CheckupCreate, CheckupUpdate, CheckupRead
from app.database import db
from app.rents.repository import rent_repo


class CheckupRepository(AbstractRepository[CheckupModel, CheckupCreate, CheckupUpdate]):
    def __init__(self):
        super().__init__(CheckupModel, db["checkup"])
        self.response_model = CheckupRead
        self.rent_full_read = rent_repo.read_pipeline
        # self.read_pipeline = [
        #     {
        #         "$lookup": {
        #             "from": "rents",  # С какой коллекцией соединяем
        #             "localField": "rent_id",  # Поле-ссылка в текущей коллекции
        #             "foreignField": "_id",  # Поле-цель в чужой коллекции
        #             "as": "rent"  # Имя поля, в которое запишем результат
        #         }
        #     },
        #     {
        #         "$unwind": {
        #             "path": "$rent",
        #             "preserveNullAndEmptyArrays": True
        #         }
        #     }
        # ]
        self.read_pipeline = [
            {
                "$lookup": {
                    "from": "rents",
                    "let": {"r_id": "$rent_id"},  # Запоминаем ID аренды из текущей коллекции
                    "pipeline": [
                        # Находим конкретный Rent в коллекции 'rents'
                        {"$match": {"$expr": {"$eq": ["$_id", "$$r_id"]}}},

                        # Вставляем ВСЕ стадии из rent пайплайна
                        # Звездочка распакует
                        *self.rent_full_read
                    ],
                    "as": "rent"
                }
            },
            {
                "$unwind": {
                    "path": "$rent",
                    "preserveNullAndEmptyArrays": True
                }
            }
        ]


checkup_repo = CheckupRepository()
