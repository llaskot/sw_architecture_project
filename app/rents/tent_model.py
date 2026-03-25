from typing import Annotated

from beanie import Document, Indexed, PydanticObjectId, Link
from pydantic import EmailStr

from app.auto_models import AutoModel
from app.autos import Car
from app.users import User


class Rent(Document):
    """Rent model"""

    car: Link[Car]
    client: Link[User]
    user_dock: str
    days_qty: int

    class Settings:
        name = "rents"