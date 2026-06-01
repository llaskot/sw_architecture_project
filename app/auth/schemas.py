from typing import Union, Optional

from pydantic import EmailStr, Field, BaseModel

from app.users import UserResponseAdm


class ConfirmationCode(BaseModel):
    conf_code: str = Field(min_length=6, max_length=6)

class ChangePassword(BaseModel):
    conf_code: str = Field(min_length=6, max_length=6)
    new_password: str = Field(min_length=6, max_length=50)


class LoginResponse(BaseModel):
    user: UserResponseAdm
    access_token: str

class PassRestore(BaseModel):
    """Restore password request scheme"""
    login: Union[EmailStr, str] = Field(..., min_length=5, max_length=50)


class RegisterResponse(BaseModel):
    success: bool
    email: EmailStr

class ConfirmResponse(BaseModel):
    success: bool
    message: Optional[str] = None