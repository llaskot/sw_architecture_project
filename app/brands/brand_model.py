from typing import Optional


from pydantic import BaseModel,  ConfigDict
from pydantic import Field
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
