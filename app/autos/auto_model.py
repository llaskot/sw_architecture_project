from typing import Annotated

from beanie import Document, Indexed, PydanticObjectId, Link
from pydantic import EmailStr

from app.auto_models import AutoModel


class Car(Document):
    """Specific vehicle instance (the 'iron')"""

    model_id: Link[AutoModel]

    # Denormalization
    brand_name: str
    model_name: str
    category: str

    # Identification
    vin: Annotated[str, Indexed(unique=True)]  # Unique vehicle ID
    plate_number: Annotated[str, Indexed(unique=True)]  # License plate

    # Characteristics
    year: int  # Production year
    color: str
    mileage: int  # Current odometer reading

    # Business
    price_per_day: float
    available: bool = True
    in_use: bool = False

    class Settings:
        name = "cars"
