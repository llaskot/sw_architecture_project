from .auto_model_model import AutoModel
from .schemas import AutoModelUpdate, AutoModelCreate, AutoModelRead
from app.database import db
from app.abstracts import AbstractRepository


class AutoModelRepository(AbstractRepository[AutoModel, AutoModelCreate, AutoModelUpdate]):
    def __init__(self):
        super().__init__(AutoModel, db["auto_model"])
        self.response_model = AutoModelRead
        self.read_pipeline = [
            {
                "$lookup": {
                    "from": "brand",  # С какой коллекцией соединяем
                    "localField": "brand_id",  # Поле-ссылка в текущей коллекции (auto_model)
                    "foreignField": "_id",  # Поле-цель в чужой коллекции (brand)
                    "as": "brand"  # Имя поля, в которое запишем результат
                }
            },
            {
                "$unwind": {
                    "path": "$brand",
                    "preserveNullAndEmptyArrays": True
                }
            }
        ]


auto_model_repo = AutoModelRepository()
