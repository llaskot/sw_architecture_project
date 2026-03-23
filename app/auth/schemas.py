from typing import Annotated, Union

from pydantic import EmailStr, Field, BaseModel

from app.users import UserResponse


class ConfirmationCode(BaseModel):
    conf_code: str = Field(min_length=6, max_length=6)

class LoginResponse(BaseModel):
    user: UserResponse
    access_token: str

class LoginDto(BaseModel):
    login: Union[EmailStr, str] = Field(..., min_length=5, max_length=50)
    password: str = Field(..., min_length=6, max_length=50)