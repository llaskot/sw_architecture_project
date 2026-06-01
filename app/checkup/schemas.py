from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic import Field
from pydantic_mongo import ObjectIdField

from .checkup_model import CheckupModel
from app.rents import RentRead


class CheckupRequest(BaseModel):
    """Registration scheme"""
    rent_id: ObjectIdField = Field(..., description="Exists rent ID")
    summary: str = Field(..., min_length=1)
    notis: str = Field(..., min_length=0)
    price: float = Field(..., ge=0)
    model_config = ConfigDict(arbitrary_types_allowed=True)


class CheckupCreate(CheckupRequest):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CheckupUpdate(BaseModel):
    """Update scheme"""
    rent_id: Optional[ObjectIdField] = Field(None, description="Exists rent ID")
    summary: Optional[str] = Field(None, min_length=1)
    notis: Optional[str] = Field(None, min_length=0)
    price: Optional[float] = Field(None, ge=0)
    model_config = ConfigDict(arbitrary_types_allowed=True)




class CheckupRead(CheckupModel):
    rent: RentRead | None = None
