from pydantic import BaseModel, Field, ConfigDict
from beanie import PydanticObjectId, Link
from typing import Annotated

from app.auto_models import AutoModel


class CarCreate(BaseModel):
    # Связь с моделью
    model_id: Link[AutoModel]


    brand_name: str = Field(..., min_length=1)
    model_name: str = Field(..., min_length=1)
    category: str

    # Идентификация
    vin: str = Field(..., min_length=17, max_length=17)
    plate_number: str = Field(..., min_length=4)

    # Характеристики
    year: int = Field(..., ge=1900, le=2222)
    color: str = Field(..., min_length=2)
    mileage: int = Field(..., ge=0)

    # Бизнес-логика
    price_per_day: float
    available: bool = True
    in_use: bool = False
