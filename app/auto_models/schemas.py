from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic import Field
from pydantic_mongo import ObjectIdField

from app.auto_models.auto_model_model import CarCategory, AutoModel
from app.brands import Brand




class AutoModelCreate(BaseModel):
    """Registration scheme"""
    brand_id: ObjectIdField = Field(..., description="Exists brand ID")
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=6)
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
