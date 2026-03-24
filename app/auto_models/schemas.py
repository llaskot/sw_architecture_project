from enum import Enum

from beanie import PydanticObjectId
from pydantic import BaseModel
from pydantic import Field


class CarCategory(str, Enum):
    ECONOMY = "economy"
    STANDARD = "standard"
    BUSINESS = "business"
    PREMIUM = "premium"
    LUXURY = "luxury"
    SUV = "suv"

class AutoModelCreate(BaseModel):
    """Registration scheme"""
    brand_id: PydanticObjectId = Field(..., description="exists brand ID")
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=6)
    category: CarCategory

