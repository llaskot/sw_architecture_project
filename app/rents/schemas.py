from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel


class RentCreate(BaseModel):

    car: PydanticObjectId
    client: PydanticObjectId
    user_dock: Optional[str] = "AAAAAA"
    days_qty: Optional[int] = 5