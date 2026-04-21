from enum import Enum
from typing import Optional, Annotated

from bson import ObjectId

from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict, field_serializer, BeforeValidator, WithJsonSchema
from pydantic_mongo import ObjectIdField


class RentStage(str, Enum):
    ORDERED = "ordered"
    BOOKED = "booked"
    REFUSED = "refused"
    PAID = "paid"
    INPROCESS = "rented"
    CLOSED = "closed"

# ObjectIdField = Annotated[
#     ObjectId,
#     BeforeValidator(lambda x: ObjectId(x) if ObjectId.is_valid(str(x)) else x),
#     WithJsonSchema({"type": "string", "example": "69dcdad6fde5b719337b0dc3"})
# ]


class Rent(BaseModel):
    """Rent model"""
    id: Optional[ObjectIdField] = Field(None, alias="_id")
    car_id: ObjectIdField = Field(..., description="Reference to car collection")
    client_id: ObjectIdField = Field(..., description="Reference to user collection")
    driver: bool = False

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_by: Optional[ObjectIdField] = Field(None, description="Reference to user collection")
    stage: RentStage = RentStage.ORDERED
    comment: Optional[str] = Field(None, description="Manager Comment")


    user_dock: str
    start_date: datetime
    days_qty: int
    total_price: float
    active: bool = True

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True
    )
    # 
    # @field_serializer("id", "car_id", 'client_id', 'updated_by')
    # def serialize_id(self, v: ObjectId, _info):
    #     return str(v) if v else None