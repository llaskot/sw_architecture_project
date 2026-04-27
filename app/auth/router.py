
from fastapi import APIRouter, Response, Request, HTTPException
from pydantic import ValidationError
from pymongo.errors import DuplicateKeyError, PyMongoError

# from pymongo.errors import DuplicateKeyError, PyMongoError
#
from app.auth.schemas import LoginResponse, ConfirmationCode, LoginDto, RegisterResponse
# from app.auth.service import AuthService
# from app.users import UserCreate, User, UserPermissionsDto
from fastapi import APIRouter

from app.auth.service import AuthService
from app.mailer.decorators import debug_request_response, debug_response
from app.users.schemas import UserRegistrate, UserResponseAdm
from app.users.service import UserService

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/register", response_model=RegisterResponse)
@debug_response
def registrate_user(user_data: UserRegistrate, response: Response):
    auth_service = AuthService()
    try:
        code, token = auth_service.register_new_user(user_data)
        response.set_cookie(
            key="register_token",
            value=token,
            httponly=True,
            samesite="lax",
            path="/auth",
            max_age=1200
        )
        return {"success": True, "cod_for_test": code, "email": user_data.email}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/register/confirm",
             response_model=LoginResponse
             )
async def save_user(data: ConfirmationCode,
                    request: Request,
                    response: Response):
    register_token = request.cookies.get("register_token")
    auth_service = AuthService()
    if not register_token:
        raise HTTPException(status_code=400, detail="Confirmation code expired")
    try:
        user = await auth_service.create_user(data, register_token)
        access_token = auth_service.prepare_tokens(user, response)
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
    auth_service = AuthService()
    try:
        user = await auth_service.refresh(refresh_token)
        access_token = auth_service.prepare_tokens(user, response)
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
    auth_service = AuthService()
    try:
        user = await auth_service.login_user(data)
        access_token = auth_service.prepare_tokens(user, response)
        return {"user": user, "access_token": access_token}
    except HTTPException as e:
        raise e from e
    except Exception as e:
        if isinstance(e, PyMongoError):
            raise HTTPException(status_code=500, detail=f"Database error:\n {str(e)}") from e
        raise HTTPException(status_code=500, detail=f"Server error: \n{str(e)}") from e


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="refresh_token",
        path="/auth/refresh",
        httponly=True,
        samesite="lax"
    )
    return {"detail": "Successfully logged out"}

