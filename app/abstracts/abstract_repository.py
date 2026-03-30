from typing import Generic, TypeVar, Type, List, Optional

from beanie import PydanticObjectId, Document
from beanie.odm.operators.update.general import Set
from pydantic import BaseModel

from app.brands.brand_model import Brand

T = TypeVar("T", bound=Document)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class AbstractRepository(Generic[T, CreateSchema, UpdateSchema]):
    def __init__(self, model: Type[T]):
        self.model = model

    async def create(self, create_dto: CreateSchema) -> T:
        new_item: Brand = self.model(**create_dto.model_dump())
        await new_item.insert()
        return new_item

    async def get_all(self) -> list[T]:
        return await self.model.find_all().to_list()

    async def get_by_id(self, item_id: PydanticObjectId) -> Optional[T]:
        return await self.model.get(item_id)

    async def update(self, item_id: PydanticObjectId, update_dto: UpdateSchema) -> Optional[T]:
        update_data = update_dto.model_dump(exclude_unset=True)
        updated_item = await self.model.find_one(self.model.id == item_id).update(
            Set(update_data),
            response_type=self.model
        )
        return updated_item

    async def delete(self, item_id: PydanticObjectId):
        return await self.model.find_one(self.model.id == item_id).delete()
