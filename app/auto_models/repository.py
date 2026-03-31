from app.auto_models import AutoModel
from app.abstracts.abstract_repository import AbstractRepository
from app.auto_models.schemas import AutoModelUpdate, AutoModelCreate


class AutoModelRepository(AbstractRepository[AutoModel, AutoModelCreate, AutoModelUpdate]):
    def __init__(self):
        # Передаем саму модель Brand в конструктор родителя
        super().__init__(AutoModel)


auto_model_repo = AutoModelRepository()
