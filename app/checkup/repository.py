from .checkup_model import CheckupModel
from .schemas import CheckupCreate, CheckupUpdate, CheckupRead
from app.database import db
from app.abstracts import AbstractRepository
from app.rents import rent_repo


class CheckupRepository(AbstractRepository[CheckupModel, CheckupCreate, CheckupUpdate]):
    def __init__(self):
        super().__init__(CheckupModel, db["checkup"])
        self.response_model = CheckupRead
        self.rent_full_read = rent_repo.read_pipeline
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
