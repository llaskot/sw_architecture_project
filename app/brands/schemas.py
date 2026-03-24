from pydantic import BaseModel
from pydantic import Field


class BrandCreate(BaseModel):
    """Registration scheme"""
    name: str = Field(..., min_length=1)
    country: str = Field(..., min_length=3)
    description: str = Field(..., min_length=6)