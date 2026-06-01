from typing import Any

from bson import ObjectId, json_util

from .auto_model import Car
from .schemas import CarCreate, CarUpdate, CarRead, SortOrder, AllCarsResponse
from app.database import db
from app.abstracts import AbstractRepository
from app.auto_models import CarCategory

class CarRepository(AbstractRepository[Car, CarCreate, CarUpdate]):
    def __init__(self):
        super().__init__(Car, db['cars'])
        self.response_model = CarRead
        self.read_pipeline = [
            # 1. Достаем модель
            {
                "$lookup": {
                    "from": "auto_model",
                    "localField": "model_id",
                    "foreignField": "_id",
                    "as": "model"
                }
            },
            # 2. Разворачиваем
            {
                "$unwind": {
                    "path": "$model",
                    "preserveNullAndEmptyArrays": True
                }
            },
            # 3. Джоиним бренд (БЕЗ удаления модели перед этим!)
            {
                "$lookup": {
                    "from": "brand",
                    "localField": "model.brand_id",
                    "foreignField": "_id",
                    "as": "model.brand"
                }
            },
            {
                "$unwind": {
                    "path": "$model.brand",
                    "preserveNullAndEmptyArrays": True
                }
            },
            # 4. ФИНАЛЬНАЯ ОЧИСТКА (делаем один раз в самом конце)
            {
                "$addFields": {
                    "model": {
                        "$cond": [
                            {"$ifNull": ["$model._id", False]},
                            "$model",
                            "$$REMOVE"  # Если нет ID модели, удаляем всё дерево model целиком
                        ]
                    }
                }
            }
        ]

    def get_set_pipeline(self,
                         brand_ids: list[str] = None,
                         categories: list[CarCategory] = None,
                         search: str = None,
                         sort_price: SortOrder = None,  # поле для сортировки
                         sort_model: SortOrder = None,
                         hide_inactive: bool = True,
                         page: int = 1,
                         limit: int = 2
                         ):
        pipeline: list[dict] = self.read_pipeline.copy()

        # 1. Фильтрация (Match)
        match_filter: dict[str, Any] = {"active": hide_inactive}
        if brand_ids:
            match_filter["model.brand._id"] = {"$in": [ObjectId(brand) for brand in brand_ids]}
        if categories:
            match_filter["model.category"] = {"$in": categories}
        if search:
            match_filter["model.name"] = {"$regex": search, "$options": "i"}
        pipeline.append({"$match": match_filter})

        sort_dict = {}
        if sort_model:
            sort_dict["model.name"] = -1 if sort_model == "desc" else 1
        if sort_price:
            sort_dict["price_per_day"] = -1 if sort_price == "desc" else 1
        sort_dict["_id"] = 1
        pipeline.append({"$sort": sort_dict})

        # ПАГИНАЦИЯ
        skip = (page - 1) * limit
        pipeline.append({
            "$facet": {
                "total_count": [{"$count": "count"}],  # Считаем общее кол-во
                "data": [  # Забираем кусок данных
                    {"$skip": skip},
                    {"$limit": limit}
                ]
            }
        })
        return pipeline

    async def get_all_set(self,
                          brand_ids: list[str],
                          categories: list[CarCategory],
                          search: str,
                          sort_price: SortOrder,
                          sort_model: SortOrder,
                          hide_inactive: bool,
                          page: int,
                          limit: int
                          ) -> AllCarsResponse:
        pipeline: list[dict] = self.get_set_pipeline(
            brand_ids,
            categories,
            search,
            sort_price,
            sort_model,
            hide_inactive,
            page,
            limit)
        res = await db['cars'].aggregate(pipeline).to_list()
        return AllCarsResponse(
            total=res[0]["total_count"][0]["count"],
            page=page,
            limit=limit,
            items=[self.response_model.model_validate(r) for r in res[0]["data"]]
        )


car_repo = CarRepository()
