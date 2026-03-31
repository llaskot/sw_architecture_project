from app.brands import Brand
from app.abstracts.abstract_repository import AbstractRepository
from app.brands.schemas import BrandCreate, BrandUpdate


class BrandRepository(AbstractRepository[Brand, BrandCreate, BrandUpdate]):
    def __init__(self):
        # Передаем саму модель Brand в конструктор родителя
        super().__init__(Brand)

    # async def get_by_name(self, name: str) -> Optional[Brand]:
    #     return await self.model.find_one({"name": name})

brand_repo = BrandRepository()