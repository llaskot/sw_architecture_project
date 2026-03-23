from typing import Annotated, Union

from beanie import Document, PydanticObjectId, Indexed
from pydantic import EmailStr, Field, BaseModel


class User(Document):
    """DB schema"""
    email: Annotated[EmailStr, Indexed(unique=True)]
    login: Annotated[str, Indexed(unique=True)]
    password: str
    first_name: str
    last_name: str
    is_active: bool = True
    is_admin: bool = False
    is_manager: bool = False

    class Settings:
        name = "users"