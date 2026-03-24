from typing import Annotated

from beanie import Document, Indexed

class Brand(Document):
    """DB schema"""
    name: Annotated[str, Indexed(unique=True)]
    country: str
    description: str

    class Settings:
        name = "brand"