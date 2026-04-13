from pydantic import BaseModel

class AbstrDelete(BaseModel):
    active: bool = False