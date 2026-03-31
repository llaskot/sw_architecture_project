from enum import Enum
from typing import Annotated

from beanie import Document, Indexed, Link

from app.brands.brand_model import Brand

class CarCategory(str, Enum):
    ECONOMY = "economy"
    STANDARD = "standard"
    BUSINESS = "business"
    PREMIUM = "premium"
    LUXURY = "luxury"
    SUV = "suv"


class AutoModel(Document):
    """DB schema"""
    brand_id: Link[Brand]
    name: Annotated[str, Indexed(unique=True)]
    description: str
    category: CarCategory
    class Settings:
        name = "auto_model"


