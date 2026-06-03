from bson import ObjectId
from fastapi import HTTPException

from app.checkup.schemas import CheckupRead
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

    async  def get_checkup_by_rent(self, rent_id: str) -> CheckupRead | None:
        pipeline = getattr(self, "read_pipeline", None)

        match_stage = {"$match": {"rent_id": ObjectId(rent_id)}}
        cursor = self.collection.aggregate([match_stage] + pipeline)
        result = await cursor.to_list(length=1)
        document = result[0] if result else None
        if not document:
            raise HTTPException(status_code=404, detail="Checkup not found")
        return self.response_model.model_validate(document)


checkup_repo = CheckupRepository()
