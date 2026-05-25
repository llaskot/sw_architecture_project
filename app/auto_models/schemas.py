from enum import Enum
from typing import Optional, Annotated

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, BeforeValidator, WithJsonSchema
from pydantic import Field
from pydantic_mongo import ObjectIdField

from app.auto_models.auto_model_model import CarCategory, AutoModel
from app.brands import Brand

# BrandID = Annotated[
#     ObjectIdField,
#     BeforeValidator(lambda x: ObjectIdField(x) if ObjectIdField.is_valid(str(x)) else x),
#     WithJsonSchema({"type": "string", "example": "69dcdad6fde5b719337b0dc3"})
# ]


class AutoModelCreate(BaseModel):
    """Registration scheme"""
    brand_id: ObjectIdField = Field(..., description="Exists brand ID")
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=6)
    # category: CarCategory = Field(..., description="Category of the car")
    category: CarCategory = Field(
        ...,
        description="Allowed: economy, standard, business, premium, luxury, suv",
        json_schema_extra={"example": "economy"}
    )
    model_config = ConfigDict(arbitrary_types_allowed=True)

class AutoModelUpdate(BaseModel):
    """Update scheme"""
    brand_id: Optional[ObjectIdField] = Field(None, description="exists brand ID")
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, min_length=6)
    active: Optional[bool] = Field(None, description="is active")
    category: Optional[CarCategory] = Field(
        None,
        description="Allowed: economy, standard, business, premium, luxury, suv",
        json_schema_extra={"example": "economy"}
    )
    model_config = ConfigDict(arbitrary_types_allowed=True)


class AutoModelRead(AutoModel):
    brand: Brand | None = None
