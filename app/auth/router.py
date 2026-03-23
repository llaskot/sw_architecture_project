import logging
from typing import Final

from fastapi import HTTPException
from fastapi import APIRouter, Response, Request
from pymongo.errors import DuplicateKeyError, PyMongoError

from app.auth.schemas import LoginResponse, ConfirmationCode, LoginDto
from app.auth.service import AuthService
from app.users import UserCreate, User, UserPermissionsDto

router = APIRouter(prefix="/auth", tags=["Users"])
REFRESH_AGE: Final = 48 * 60 * 60


@router.post("/register")
def registrate_user(user_data: UserCreate, response: Response):
    try:
        code, token = AuthService.register_new_user(user_data)
        response.set_cookie(
            key="register_token",
            value=token,
            httponly=True,
            samesite="lax",
            path="/auth",
            max_age=1200
        )
        return {"success": True, "cod_for_test": code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/register/confirm", response_model=LoginResponse)
async def save_user(data: ConfirmationCode,
                    request: Request,
                    response: Response):
    register_token = request.cookies.get("register_token")

    try:
        user = await AuthService.create_user(data, register_token)
        access_token = prepare_tokens(user, response)
        return {"user": user, "access_token": access_token}
    except HTTPException as e:
        raise e from e
    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"User already exists\n{str(e)}") from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        if isinstance(e, PyMongoError):
            raise HTTPException(status_code=500, detail=f"Database error:\n {str(e)}") from e
        raise HTTPException(status_code=500, detail=f"Server error: \n{str(e)}") from e


@router.get("/refresh")
async def refresh(request: Request,
                  response: Response):
    refresh_token = request.cookies.get("refresh_token")
    try:
        user = await AuthService.refresh(refresh_token)
        access_token = prepare_tokens(user, response)
        return {"access_token": access_token}
    except HTTPException as e:
        raise e from e
    except Exception as e:
        if isinstance(e, PyMongoError):
            raise HTTPException(status_code=500, detail=f"Database error:\n {str(e)}") from e
        raise HTTPException(status_code=500, detail=f"Server error: \n{str(e)}") from e


@router.post("/login", response_model=LoginResponse)
async def login(data: LoginDto,
                response: Response):
    try:
        user = await AuthService.login_user(data)
        access_token = prepare_tokens(user, response)
        return {"user": user, "access_token": access_token}
    except HTTPException as e:
        raise e from e
    except Exception as e:
        if isinstance(e, PyMongoError):
            raise HTTPException(status_code=500, detail=f"Database error:\n {str(e)}") from e
        raise HTTPException(status_code=500, detail=f"Server error: \n{str(e)}") from e


def prepare_tokens(user: User, response: Response):
    permissions = UserPermissionsDto.model_validate(user)
    user_payload = permissions.model_dump()
    tokens = AuthService.create_token(user_payload)
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        samesite="lax",
        path="/auth/refresh",
        max_age=REFRESH_AGE
    )
    return tokens["access_token"]

