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
    driver: Optional[bool] = Field(False, description="driver required")
    user_dock: str
    start_date: datetime
    days_qty: int = Field(1, description="rent length")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True
    )

class RentCreate(RentRequest):
    """Create rent schema"""
    client_id: ObjectIdField = Field(..., description="exists user id")
    end_date: datetime = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_by: Optional[ObjectIdField] = Field(None, description="Reference to user collection")
    stage: RentStage = RentStage.ORDERED
    comment: Optional[str] = Field(None, description="Manager Comment")
    total_price: float
    active: bool = True


class RentUpdateRequest(BaseModel):
    """Request rent schema"""
    car_id: Optional[ObjectIdField] = Field(None, description="Exists car id")
    client_id: Optional[ObjectIdField] = Field(None, description="exists user id")
    driver: Optional[bool] = Field(None, description="driver required")
    user_dock: Optional[str] = Field(None, description="user dock")
    start_date: Optional[datetime] = Field(None, description="start rent date")
    days_qty: Optional[int] = Field(None, ge=1, description="rent length")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True
    )


class RentUpdate(RentUpdateRequest):
    """Create rent schema"""
    end_date: Optional[datetime] = Field(None, description="New end date")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_by: Optional[ObjectIdField] = Field(None, description="Reference to user collection")
    total_price: Optional[float] = Field(None, description="Total price")

class ChangeStage(BaseModel):
    """Change stage schema"""
    comment: Optional[str] = Field(None, description="Manager Comment")

class UpdateStage(ChangeStage):
    """Update stage in DB"""
    stage: RentStage
    updated_by: ObjectIdField = Field(..., description="Reference to user collection")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))








class RentRead(Rent):
    car: CarRead | None = None
    client: User | None = None

