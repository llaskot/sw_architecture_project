from typing import Annotated

from fastapi import APIRouter, Response, Request

from app.auth.service import AuthService
from app.users.schemas import UserOut, UserCreate, ConfirmationCode, LoginResponse, User, LoginDto

router = APIRouter(prefix="/auth", tags=["Users"])


@router.post("/register")
def registrate_user(user_data: UserCreate, response: Response):
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


@router.post("/register/confirm", response_model=LoginResponse)
async def save_user(data: ConfirmationCode,
                    request: Request,
                    response: Response):
    register_token = request.cookies.get("register_token")

    user = await AuthService.create_user(data, register_token)
    access_token = prepare(user, response)
    return {"user": user, "access_token": access_token}


@router.get("/refresh")
async def refresh(request: Request,
                  response: Response):
    refresh_token = request.cookies.get("refresh_token")
    user = await AuthService.refresh(refresh_token)
    access_token = prepare(user, response)
    return {"access_token": access_token}


def prepare(user: User, response: Response):
    user_payload = user.model_dump(include={
        "is_active",
        "is_admin",
        "is_manager"
    })
    user_payload["id"] = str(user.id)
    tokens = AuthService.create_token(user_payload)
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        samesite="lax",
        path="/auth/refresh",
        max_age=48 * 60 * 60
    )
    return tokens["access_token"]

@router.post("/login", response_model=LoginResponse)
async def login(data: LoginDto,
                request: Request,
                  response: Response):
    user = await AuthService.login_user(data)
    access_token = prepare(user, response)
    return {"user": user,"access_token": access_token}