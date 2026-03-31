from app.abstracts import AbstractService
from app.auto_models import auto_model_repo
from app.auto_models.schemas import AutoModelCreate, AutoModelUpdate



class AutoModelService(AbstractService[AutoModelCreate, AutoModelUpdate]):
    def __init__(self):
        super().__init__(auto_model_repo)