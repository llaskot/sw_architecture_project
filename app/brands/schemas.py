from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class BrandCreate(BaseModel):
    """Registration scheme"""
    name: str = Field(..., min_length=1)
    country: str = Field(..., min_length=3)
    description: str = Field(..., min_length=6)

class BrandUpdate(BaseModel):
    """Update scheme"""
    name: Optional[str] = Field(None, min_length=1)
    country: Optional[str] = Field(None, min_length=3)
    description: Optional[str] = Field(None, min_length=6)
    active: Optional[bool]  = Field(None)
