from typing import Generic, TypeVar, Type

from beanie import PydanticObjectId
from fastapi import HTTPException
from pydantic import BaseModel

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class AbstractService(Generic[CreateSchemaType, UpdateSchemaType]):
    def __init__(self, repository):
        self.repo = repository
        self.response_schema = None

    async def create(self, data: CreateSchemaType):
        return await self.repo.create(data)

    async def update(self, item_id: PydanticObjectId, data: UpdateSchemaType ):
        res =  await self.repo.update(item_id, data)
        if not res:
            raise HTTPException(status_code=404, detail="Item not found")
        return res

    async def get_by_id(self, item_id: PydanticObjectId):
        res =  await self.repo.get_by_id(item_id)
        if not res:
            raise HTTPException(status_code=404, detail="Item not found")
        return res

    async def get_all(self):
        return await self.repo.get_all()

    async def delete(self, item_id: PydanticObjectId):
        success = await self.repo.delete(item_id)
        if not success:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"success": True}
