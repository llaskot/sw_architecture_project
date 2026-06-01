from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, field_serializer
from pydantic_mongo import ObjectIdField


class Pictures(BaseModel):
    small: str | None = None
    large: str | None = None


class Car(BaseModel):
    """Specific vehicle instance (the 'iron')"""
    id: Optional[ObjectIdField] = Field(None, alias="_id")
    model_id: ObjectIdField = Field(..., description="Reference to auto_model collection")

    # Identification
    vin: str  # Unique vehicle ID
    plate_number: str  # License plate

    # Characteristics
    year: int  # Production year
    color: str
    mileage: int  # Current odometer reading

    # Business
    price_per_day: float
    available: bool = True
    in_use: bool = False

    active: bool = True

    img: Pictures | None = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True
    )



