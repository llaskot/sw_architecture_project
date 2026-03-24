from app.auto_models import AutoModel, auto_model_repo
from app.autos import Car
from app.autos.repository import car_repo
from app.autos.schemas import CarCreate


class CarService:
    @staticmethod
    async def create_car(dto: CarCreate) -> Car:
        auto_model = await auto_model_repo.get_model_by_id(dto.model_id)
        # Merging DTO data with model info
        car_data = dto.model_dump()
        car_data.update({
            "brand_name": auto_model.brand_id.name,
            "model_name": auto_model.name,
            "category": auto_model.category
        })
        new_car = Car(**car_data)
        return await car_repo.save_car(new_car)