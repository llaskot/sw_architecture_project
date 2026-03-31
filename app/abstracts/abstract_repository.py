from typing import Generic, TypeVar, Type, List, Optional, Any

from beanie import PydanticObjectId, Document, Link
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
        return await self.fetch_links_recursive(new_item)

    async def get_all(self) -> list[T]:
        items = await self.model.find_all().to_list()
        for i in range(len(items)):
            items[i] = await self.fetch_links_recursive(items[i])
        return items

    async def fetch_links(self, item: T) -> T:
        if not item:
            return item
        for field in item.model_fields.keys():
            value = getattr(item, field)
            if isinstance(value, Link):
                ref_id = value.ref.id
                ref_model = value.document_class
                linked_doc = await ref_model.get(ref_id)
                setattr(item, field, linked_doc)
        return item

    async def fetch_links_recursive(self, item: Any) -> Any:
        if not item or not hasattr(item, "model_fields"):
            return item

        for field in item.model_fields.keys():
            value = getattr(item, field)
            if isinstance(value, Link):
                ref_id = value.ref.id
                ref_model = value.document_class
                linked_doc = await ref_model.get(ref_id)

                if linked_doc:
                    linked_doc = await self.fetch_links_recursive(linked_doc)

                setattr(item, field, linked_doc)

            elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], Link):
                processed_list = []
                for link in value:
                    doc = await link.document_class.get(link.ref.id)
                    if doc:
                        doc = await self.fetch_links_recursive(doc)
                    processed_list.append(doc)
                setattr(item, field, processed_list)

        return item


    async def get_by_id(self, item_id: PydanticObjectId) -> Optional[T]:
        res =  await self.model.get(item_id)
        return await self.fetch_links_recursive(res)

    async def update(self, item_id: PydanticObjectId, update_dto: UpdateSchema) -> Optional[T]:
        update_data = update_dto.model_dump(exclude_unset=True)
        updated_item = await self.model.find_one(self.model.id == item_id).update(
            Set(update_data),
            response_type=self.model
        )
        return await self.fetch_links_recursive(updated_item)

    async def delete(self, item_id: PydanticObjectId):
        return await self.model.find_one(self.model.id == item_id).delete()


