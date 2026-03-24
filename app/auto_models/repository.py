from typing import Type

from beanie import PydanticObjectId, Document

from app.auto_models.auto_model_model import AutoModel
from app.auto_models.schemas import AutoModelCreate


class AutoModelRepository:
    def __init__(self, model: Type[AutoModel]):
        self.model = model

    async def save_auto_model(self, create_model_dto: AutoModelCreate) -> AutoModel:
        new_model: AutoModel = self.model(**create_model_dto.model_dump())
        await new_model.insert()
        return new_model

    # async def get_all_models(self) -> list[AutoModel]:
    #     return await self.model.find(fetch_links=True).to_list()

    async def get_all_models(self) -> list[AutoModel]:
        models = await self.model.find_all().to_list()
        for m in models:
            m.brand_id = await m.brand_id.fetch()
        return models


    async def get_model_by_id(self, model_id: PydanticObjectId) -> AutoModel | None:
        mod = await self.model.get(model_id)
        mod.brand_id = await mod.brand_id.fetch()
        return mod


auto_model_repo = AutoModelRepository(AutoModel)

