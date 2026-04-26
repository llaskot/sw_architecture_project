from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Annotated

from pydantic import BaseModel, ConfigDict
from pydantic import Field
from pydantic_mongo import ObjectIdField

from app.checkup.checkup_model import CheckupModel
from app.rents.rent_model import Rent
from app.rents.schemas import RentRead


class CheckupCreate(BaseModel):
    """Registration scheme"""
    rent_id: ObjectIdField = Field(..., description="Exists rent ID")
    summary: str = Field(..., min_length=1)
    notis: str = Field(..., min_length=0)
    price: float = Field(..., ge=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_config = ConfigDict(arbitrary_types_allowed=True)

class CheckupUpdate(BaseModel):
    """Update scheme"""
    rent_id: Optional[ObjectIdField] = Field(None, description="Exists rent ID")
    summary: Optional[str] = Field(None, min_length=1)
    notis: Optional[str] = Field(None, min_length=0)
    price: Optional[float] = Field(None, ge=0)
    model_config = ConfigDict(arbitrary_types_allowed=True)




class CheckupRead(CheckupModel):
    rent: RentRead | None = None
