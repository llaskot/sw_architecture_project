from typing import Annotated, Optional

from bson import ObjectId
from pydantic import EmailStr, BaseModel, ConfigDict, field_serializer, Field
from pydantic_mongo import ObjectIdField


class User(BaseModel):
    """DB schema"""
    id: Optional[ObjectIdField] = Field(None, alias="_id")
    email: EmailStr
    login: str
    password: str
    first_name: str
    last_name: str
    active: bool = True
    is_admin: bool = False
    is_manager: bool = False

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        from_attributes=True
    )

    # @field_serializer("id")
    # def serialize_id(self, v: ObjectId, _info):
    #     return str(v) if v else None


