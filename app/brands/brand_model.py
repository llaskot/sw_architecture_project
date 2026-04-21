from typing import Annotated, Optional


from pydantic import BaseModel, Field, ConfigDict
from pydantic import Field, field_serializer
from bson import ObjectId
from pydantic_mongo import ObjectIdField


class Brand(BaseModel):
    id: Optional[ObjectIdField] = Field(None, alias="_id")
    name: str
    country: str
    description: str
    active: bool = True

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True
    )
    #
    # @field_serializer("id")
    # def serialize_id(self, v: ObjectId, _info):
    #     return str(v) if v else None