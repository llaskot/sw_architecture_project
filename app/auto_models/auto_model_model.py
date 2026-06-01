from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, field_serializer, ConfigDict, Field
from pydantic_mongo import ObjectIdField


class CarCategory(str, Enum):
    ECONOMY = "economy"
    STANDARD = "standard"
    BUSINESS = "business"
    PREMIUM = "premium"
    LUXURY = "luxury"
    SUV = "suv"


class AutoModel(BaseModel):
    """DB schema"""
    id: Optional[ObjectIdField] = Field(None, alias="_id")
    brand_id: ObjectIdField = Field(..., description="Reference to Brand collection")
    name: str
    description: str
    category: CarCategory
    active: bool = True
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True
    )



