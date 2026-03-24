from typing import Type

from beanie import PydanticObjectId, Document

from app.auto_models.auto_model_model import AutoModel
from app.auto_models.schemas import AutoModelCreate
from app.autos import Car


class AutoModelRepository:
    def __init__(self, model: Type[Car]):
        self.model = model

    async def save_car(self, create_model_dto: AutoModelCreate) -> Car:
        new_car: Car = self.model(**create_model_dto.model_dump())
        await new_car.insert()
        return new_car



    # async def get_all_models(self) -> list[AutoModel]:
    #     models = await self.model.find_all().to_list()
    #     for m in models:
    #         m.brand_id = await m.brand_id.fetch()
    #     return models
    #
    #
    # async def get_model_by_id(self, model_id: PydanticObjectId) -> AutoModel | None:
    #     mod = await self.model.get(model_id)
    #     mod.brand_id = await mod.brand_id.fetch()
    #     return mod


car_repo = AutoModelRepository(Car)