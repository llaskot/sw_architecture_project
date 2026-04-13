
from app.brands import Brand
from app.abstracts.abstract_repository import AbstractRepository
from app.brands.schemas import BrandCreate, BrandUpdate
from app.database import db


class BrandRepository(AbstractRepository[Brand, BrandCreate, BrandUpdate]):
    def __init__(self, db):
        # Передаем саму модель Brand в конструктор родителя
        super().__init__(Brand, db["brand"])


brand_repo = BrandRepository(db)