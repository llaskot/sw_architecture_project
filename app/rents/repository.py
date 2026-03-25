from typing import Type

from app.rents.schemas import RentCreate
from app.rents.tent_model import Rent


class AutoModelRepository:
    def __init__(self, model: Type[Rent]):
        self.model = model

    async def save_rent(self, create_rent_dto: RentCreate) -> Rent:
        new_rent: Rent = self.model(**create_rent_dto.model_dump())
        await new_rent.insert()
        return new_rent



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


rent_repo = AutoModelRepository(Rent)