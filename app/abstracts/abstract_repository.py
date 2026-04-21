from typing import Generic, TypeVar, Type, List, Optional, Any

from pydantic import BaseModel
from fastapi import HTTPException
from pymongo.asynchronous.collection import ReturnDocument

from app.abstracts.abstract_chemas import AbstrDelete

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

T = TypeVar("T", bound=BaseModel)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class AbstractRepository(Generic[T, CreateSchema, UpdateSchema]):
    def __init__(self, model: Type[T], collection: AsyncIOMotorCollection):
        self.model = model
        self.collection = collection
        self.response_model = model
        self.read_pipeline = None

    async def create(self, create_dto: CreateSchema) -> T:
        new_item = create_dto.model_dump(mode='python', by_alias=True)
        new_item['active'] = True
        res = await self.collection.insert_one(new_item)
        new_item["_id"] = res.inserted_id
        return self.model.model_validate(new_item)

    async def get_all(self, hide_inactive: bool = True) -> list[Any]:
        match_stage = {"$match": {}}
        if hide_inactive:
            match_stage["$match"]["active"] = True

        if self.read_pipeline:
            full_pipeline = [match_stage] + self.read_pipeline
            cursor = self.collection.aggregate(full_pipeline)
        else:
            cursor = self.collection.find(match_stage["$match"])
        documents = await cursor.to_list(length=None)
        return [self.response_model.model_validate(doc) for doc in documents]


    async def get_by_id(self, item_id: ObjectId, hide_inactive: bool = True) -> Any:
        pipeline = getattr(self, "read_pipeline", None)

        match_stage = {"$match": {"_id": item_id}}
        if hide_inactive:
            match_stage["$match"]["active"] = True
        if pipeline:
            # Если нашли пайплайн в наследнике — ебашим агрегацию
            cursor = self.collection.aggregate([match_stage] + pipeline)
            result = await cursor.to_list(length=1)
            document = result[0] if result else None
        else:
            # Если нет — обычный find_one
            document = await self.collection.find_one(match_stage["$match"])

        if document is None: return None
        return self.response_model.model_validate(document)


    async def update(self, item_id: ObjectId, update_dto: UpdateSchema, hide_inactive: bool = None) -> Optional[T]:
        query = {"_id": item_id}
        if hide_inactive is None:
            query["active"] = True
        else:
            query["active"] = hide_inactive
        update_data = update_dto.model_dump(exclude_unset=True)
        print(query)
        updated_item = await self.collection.find_one_and_update(
            query,
            {"$set": update_data},  # Оператор $set обновляет только указанные поля
            return_document=ReturnDocument.AFTER
        )
        if not updated_item:
            return None
        return self.model.model_validate(updated_item)


    async def delete(self, item_id: ObjectId):
        dto = AbstrDelete(
            active=False,
        )
        return await self.update(item_id, dto, hide_inactive=True)


