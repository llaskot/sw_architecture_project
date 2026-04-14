from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Annotated

from bson import ObjectId
from pydantic import BaseModel, Field, BeforeValidator, WithJsonSchema, ConfigDict, field_serializer

from app.autos.schemas import CarRead
from app.rents.rent_model import Rent
from app.users.user_model import User

PyObjectID = Annotated[
    ObjectId,
    BeforeValidator(lambda x: ObjectId(x) if ObjectId.is_valid(str(x)) else x),
    WithJsonSchema({"type": "string", "example": "69dcdad6fde5b719337b0dc3"})
]




class RentCreate(BaseModel):
    """Create rent schema"""
    car_id: PyObjectID = Field(..., description="Exists car id")
    client_id: PyObjectID = Field(..., description="exists user id")
    driver: Optional[bool] = Field(False, description="driver required")
    user_dock: str
    start_date: datetime
    days_qty: int = Field(1, description="rent length")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True
    )

    # @field_serializer("car_id", 'client_id')
    # def serialize_id(self, v: ObjectId, _info):
    #     return str(v) if v else None

class RentUpdate(BaseModel):
    """Create rent schema"""
    car_id: PyObjectID = Field(..., description="Exists car id")
    client_id: PyObjectID = Field(..., description="exists user id")
    driver: Optional[bool] = Field(False, description="driver required")
    user_dock: str
    start_date: datetime
    days_qty: int = Field(1, description="rent length")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True
    )

    # @field_serializer("car_id", 'client_id')
    # def serialize_id(self, v: ObjectId, _info):
    #     return str(v) if v else None


class RentRead(Rent):
    car: CarRead | None = None
    client: User | None = None
    @field_serializer("id", "car_id", 'client_id', 'updated_by')
    def serialize_id(self, v: ObjectId, _info):
        return str(v) if v else None