from fastapi import Request, HTTPException
from app.auth.service import AuthService
from app.users import UserPermissionsDto


async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    token = auth_header.split(" ")[1]

    payload = AuthService.decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid or expired token")


    return UserPermissionsDto(**payload)