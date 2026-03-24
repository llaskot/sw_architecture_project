from app.auto_models import AutoModel
from app.autos import Car
from app.autos.schemas import CarCreate


class CarService:
    @staticmethod
    async def create_car(dto: CarCreate) -> Car:
        # Fetching linked model to get its details
        auto_model = await AutoModel.get(dto.model_id.ref.id)

        # Merging DTO data with model info
        car_data = dto.model_dump()
        car_data.update({
            "brand_name": auto_model.brand_id.name,
            "model_name": auto_model.name,
            "category": auto_model.category
        })

        # Inserting into DB
        new_car = Car(**car_data)
        return await new_car.insert()