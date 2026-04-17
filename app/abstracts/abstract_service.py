from typing import Generic, TypeVar, Type, Any

# from beanie import PydanticObjectId
from fastapi import HTTPException
from pydantic import BaseModel
from bson import ObjectId

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class AbstractService(Generic[CreateSchemaType, UpdateSchemaType]):
    def __init__(self, repository: Any):
        self.repo = repository

    async def create(self, data: CreateSchemaType):
        await self.check(data)
        return await self.repo.create(data)


    async def update(self, item_id: str | ObjectId, data: UpdateSchemaType,  hide_inactive: bool = None ):
        await self.check(data)
        if isinstance(item_id, str):
            try:
                item_id = ObjectId(item_id)
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid ID format")
        res =  await self.repo.update(item_id, data, hide_inactive)
        if not res:
            raise HTTPException(status_code=404, detail="Item not found")
        return res


    async def get_by_id(self, item_id: str | ObjectId, hide_inactive: bool = True):
        print(item_id)
        if isinstance(item_id, str):
            try:
                item_id = ObjectId(item_id)
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid ID format")
        res = await self.repo.get_by_id(item_id, hide_inactive)
        if not res:
            raise HTTPException(status_code=404, detail="Item not found")
        return res

    async def get_all(self, hide_inactive: bool = True) :
        return await self.repo.get_all(hide_inactive)

    async def delete(self, item_id: str | ObjectId):
        if isinstance(item_id, str):
            try:
                item_id = ObjectId(item_id)
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid ID format")
        success = await self.repo.delete(item_id)
        if not success:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"success": True}

    async def check(self, data: CreateSchemaType | UpdateSchemaType):
        pass