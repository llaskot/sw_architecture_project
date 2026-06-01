from enum import Enum
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator, WithJsonSchema
from typing import Annotated, Optional

from pydantic_mongo import ObjectIdField

from .auto_model import Car, Pictures
from app.auto_models import AutoModelRead


ModelID = Annotated[
    ObjectIdField,
    BeforeValidator(lambda x: ObjectIdField(x) if ObjectIdField.is_valid(str(x)) else x),
    WithJsonSchema({"type": "string", "example": "69dcdad6fde5b719337b0dc3"})
]

class CarCreate(BaseModel):
    model_id: ModelID = Field(..., description="Exists model ID")

    vin: str = Field(..., min_length=17, max_length=17)
    plate_number: str = Field(..., min_length=4)

    year: int = Field(..., ge=1900, le=2222)
    color: str = Field(..., min_length=2)
    mileage: int = Field(..., ge=0)

    price_per_day: float
    available: bool = True
    in_use: bool = False

    img: str = None

    model_config = ConfigDict(arbitrary_types_allowed=True)



class CarUpdate(BaseModel):
    model_id: Optional[ModelID] = Field(None, description="exists model ID")

    vin: Optional[str] = Field(None, min_length=17, max_length=17)
    plate_number: Optional[str] = Field(None, min_length=4)

    year: Optional[int] = Field(None, ge=1900, le=2222)
    color: Optional[str] = Field(None, min_length=2)
    mileage: Optional[int] = Field(None, ge=0)

    price_per_day: Optional[float] = Field(None)
    available: Optional[bool] = Field(None)
    in_use: Optional[bool] = Field(None)

    img: Optional[Pictures] = Field(None)

    model_config = ConfigDict(arbitrary_types_allowed=True)
    active: Optional[bool]  = Field(None)



class CarRead(Car):
    model: AutoModelRead | None = None


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"
    NONE = 'none'

class AllCarsResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: list[CarRead]
