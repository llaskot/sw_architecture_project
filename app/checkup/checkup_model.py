from datetime import datetime, timezone
from typing import  Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic_mongo import ObjectIdField



class CheckupModel(BaseModel):
    """DB schema"""
    id: Optional[ObjectIdField] = Field(None, alias="_id")
    rent_id: ObjectIdField = Field(..., description="Exists rent ID")
    summary: str = Field(..., min_length=1)
    notis: str = Field(..., min_length=0)
    price: float = Field(..., ge=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_config = ConfigDict(arbitrary_types_allowed=True)


