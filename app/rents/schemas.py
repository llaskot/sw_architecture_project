from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field,  ConfigDict
from pydantic_mongo import ObjectIdField

from app.autos.schemas import CarRead
from app.rents.rent_model import Rent, RentStage
from app.users.user_model import User






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

    car: CarRead | None = None
    client: User | None = None

