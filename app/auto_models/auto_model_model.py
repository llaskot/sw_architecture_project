from enum import Enum
from typing import Annotated, Optional

from bson import ObjectId
from pydantic import BaseModel, field_serializer, ConfigDict, Field

from app.brands.brand_model import Brand

class CarCategory(str, Enum):
    ECONOMY = "economy"
    STANDARD = "standard"
    BUSINESS = "business"
    PREMIUM = "premium"
    LUXURY = "luxury"
    SUV = "suv"


class AutoModel(BaseModel):
    """DB schema"""
    id: Optional[ObjectId] = Field(None, alias="_id")
    brand_id: ObjectId = Field(..., description="Reference to Brand collection")
    name: str
    description: str
    category: CarCategory
    active: bool = True
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    @field_serializer("id", "brand_id")
    def serialize_id(self, v: ObjectId, _info):
        return str(v) if v else None


