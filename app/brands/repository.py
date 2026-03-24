from typing import Type

from beanie import PydanticObjectId, Document

from app.brands.brand_model import Brand
from app.brands.schemas import BrandCreate


class BrandRepository:
    def __init__(self, model: Type[Brand]):
        self.model = model

    async def save_brand(self, create_brand_dto: BrandCreate) -> Brand:
        new_brand: Brand = self.model(**create_brand_dto.model_dump())
        await new_brand.insert()
        return new_brand

    async def get_all_brands(self) -> list[Brand]:
        return await self.model.find_all().to_list()

    async def get_brand_by_id(self, brand_id: PydanticObjectId) -> Brand | None:
        return await self.model.get(brand_id)



user_repo = BrandRepository(Brand)