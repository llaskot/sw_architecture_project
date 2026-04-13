from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator, WithJsonSchema
from typing import Annotated, Optional

from app.auto_models.schemas import AutoModelRead
from app.autos import Car

ModelID = Annotated[
    ObjectId,
    BeforeValidator(lambda x: ObjectId(x) if ObjectId.is_valid(str(x)) else x),
    WithJsonSchema({"type": "string", "example": "69dcdad6fde5b719337b0dc3"})
]

class CarCreate(BaseModel):
    # Связь с моделью
    model_id: ModelID = Field(..., description="Exists model ID")

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

    model_config = ConfigDict(arbitrary_types_allowed=True)



class CarUpdate(BaseModel):
    model_id: Optional[ModelID] = Field(None, description="exists model ID")

    # Идентификация
    vin: Optional[str] = Field(None, min_length=17, max_length=17)
    plate_number: Optional[str] = Field(None, min_length=4)

    # Характеристики
    year: int = Field(None, ge=1900, le=2222)
    color: str = Field(None, min_length=2)
    mileage: int = Field(None, ge=0)

    # Бизнес-логика
    price_per_day: Optional[float] = Field(None)
    available: Optional[bool] = Field(None)
    in_use: Optional[bool] = Field(None)

    model_config = ConfigDict(arbitrary_types_allowed=True)
    # active: Optional[bool]  = Field(None)



class CarRead(Car):
    model: AutoModelRead | None = None