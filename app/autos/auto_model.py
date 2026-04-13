from typing import  Optional

from bson import ObjectId
from pydantic import  BaseModel, Field, ConfigDict, field_serializer


class Car(BaseModel):
    """Specific vehicle instance (the 'iron')"""
    id: Optional[ObjectId] = Field(None, alias="_id")
    model_id: ObjectId = Field(..., description="Reference to auto_model collection")

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

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    @field_serializer("id", "model_id")
    def serialize_id(self, v: ObjectId, _info):
        return str(v) if v else None

