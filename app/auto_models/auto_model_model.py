from typing import Annotated

from beanie import Document, Indexed, Link

from app.brands.brand_model import Brand


class AutoModel(Document):
    """DB schema"""
    brand_id: Link[Brand]
    name: Annotated[str, Indexed(unique=True)]
    description: str
    category: str
    class Settings:
        name = "auto_model"