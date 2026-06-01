from fastapi import  Response, Request, HTTPException
from pymongo.errors import DuplicateKeyError, PyMongoError
from fastapi import APIRouter
from .schemas import LoginResponse, ConfirmationCode,  RegisterResponse, PassRestore, ChangePassword, \
    ConfirmResponse

from .service import AuthService
from app.mailer import  confirm_mail
from app.users import UserRegistrate, LoginDto

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/register", response_model=RegisterResponse)
@confirm_mail
def registrate_user(user_data: UserRegistrate, response: Response):
    auth_service = AuthService()
    try:
        code, token = auth_service.register_new_user(user_data)
        response.set_cookie(
            key="register_token",
            value=token,
            httponly=True,
            samesite="lax",
            # path="/auth",
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
        details = e.details
        key_value = details.get("keyValue", {})
        field_name = list(key_value.keys())[0] if key_value else "field"
        raise HTTPException(
            status_code=400,
            detail=f"User already exists! field: {field_name}") from e
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
        # path="/auth/refresh",
        httponly=True,
        samesite="lax"
    )
    return {"detail": "Successfully logged out"}


@router.post("/restore", response_model=RegisterResponse)
@confirm_mail
async def restore_password(user_data: PassRestore, response: Response):
    auth_service = AuthService()
    try:
        email, code, token = await auth_service.get_restore_code(user_data)
        response.set_cookie(
            key="restore_token",
            value=token,
            httponly=True,
            samesite="lax",
            # path="/auth/restore/confirm",
            max_age=1200
        )
        return {"success": True, "cod_for_test": code, "email": email}
    except HTTPException as e:
        raise e from e
    except Exception as e:
        if isinstance(e, PyMongoError):
            raise HTTPException(status_code=500, detail=f"Database error:\n {str(e)}") from e
        raise HTTPException(status_code=500, detail=f"Server error: \n{str(e)}") from e


@router.post("/restore/confirm",
             response_model=ConfirmResponse
             )
async def change_password(data: ChangePassword, request: Request):
    auth_service = AuthService()
    restore_token = request.cookies.get("restore_token")
    if not restore_token:
        raise HTTPException(status_code=400, detail="Confirmation code expired")
    try:
        return await auth_service.change_password(data, restore_token)
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
