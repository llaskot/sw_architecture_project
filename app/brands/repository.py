
from .brand_model import Brand
from .schemas import BrandCreate, BrandUpdate
from app.database import db
from app.abstracts import AbstractRepository



class BrandRepository(AbstractRepository[Brand, BrandCreate, BrandUpdate]):
    def __init__(self, db):
        # Передаем саму модель Brand в конструктор родителя
        super().__init__(Brand, db["brand"])


brand_repo = BrandRepository(db)