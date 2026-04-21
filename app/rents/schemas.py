from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Annotated, Any

from bson import ObjectId
from pydantic import BaseModel, Field, BeforeValidator, WithJsonSchema, ConfigDict, field_serializer, field_validator
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema
from pydantic_mongo import ObjectIdField

from app.autos.schemas import CarRead
from app.rents.rent_model import Rent, RentStage
from app.users.user_model import User

# PyObjectID = Annotated[
#     ObjectId,
#     BeforeValidator(lambda x: ObjectId(x) if ObjectId.is_valid(str(x)) else x),
#     WithJsonSchema({"type": "string", "example": "69dcdad6fde5b719337b0dc3"})
# ]




class RentRequest(BaseModel):
    """Request rent schema"""
    car_id: ObjectIdField = Field(..., description="Exists car id")
    client_id: ObjectIdField = Field(..., description="exists user id")
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



class RentCreate(RentRequest):
    """Create rent schema"""

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_by: Optional[ObjectIdField] = Field(None, description="Reference to user collection")
    stage: RentStage = RentStage.ORDERED
    comment: Optional[str] = Field(None, description="Manager Comment")
    total_price: float
    active: bool = True


class RentUpdate(BaseModel):
    """Create rent schema"""
    car_id: ObjectIdField = Field(..., description="Exists car id")
    client_id: ObjectIdField = Field(..., description="exists user id")
    driver: Optional[bool] = Field(False, description="driver required")
    user_dock: str
    start_date: datetime
    days_qty: int = Field(1, description="rent length")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True
    )



class RentRead(Rent):
    # Твои вложенные (можешь раскукожить, если надо)
    id: ObjectIdField = Field(alias="_id")
    car_id: ObjectIdField
    client_id: ObjectIdField
    # car: CarRead | None = None
    client: User | None = None

    # @field_serializer("id", "car_id", "client_id", "updated_by", check_fields=False)
    # def serialize_id(self, v: Any, _info):
    #     return str(v) if v else None

