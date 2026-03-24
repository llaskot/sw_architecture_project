
from beanie import  PydanticObjectId
from pydantic import EmailStr, Field, BaseModel, field_validator


class UserCreate(BaseModel):
    """Registration scheme"""
    email: EmailStr  # Авто-валидация формата почты
    login: str = Field(..., min_length=6, max_length=20)
    password: str = Field(..., min_length=6)
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)






class UserResponseBasic(BaseModel):
    """Response schema"""
    id: PydanticObjectId
    first_name: str
    last_name: str
    is_active: bool
    is_admin: bool
    is_manager: bool
    model_config = {
        "from_attributes": True,  # Читаем из атрибутов объекта
        "populate_by_name": True  # Если что, ищем по имени
    }

class UserResponse(UserResponseBasic):
    """Полный вариант: всё то же самое + конфиденциальные данные"""
    email: EmailStr
    login: str

class UserPermissionsDto(BaseModel):
    id: str
    is_active: bool
    is_admin: bool
    is_manager: bool

    @field_validator("id", mode="before")
    @classmethod
    def serialize_id(cls, v):
        # Если пришел ObjectId, превращаем в строку, иначе оставляем как есть
        return str(v) if v else v

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }
