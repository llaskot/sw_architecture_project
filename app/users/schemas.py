from typing import Annotated

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

class UserCreate(BaseModel):
    """Registration scheme"""
    email: EmailStr  # Авто-валидация формата почты
    login: str = Field(..., min_length=6, max_length=20)
    password: str = Field(..., min_length=6)
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)

class UserOut(BaseModel):
    """Response schema"""
    id: PydanticObjectId
    email: EmailStr
    login: str
    first_name: str
    last_name: str
    is_active: bool
    is_admin: bool
    is_manager: bool
    model_config = {
        "from_attributes": True,  # Читаем из атрибутов объекта
        "populate_by_name": True  # Если что, ищем по имени
    }