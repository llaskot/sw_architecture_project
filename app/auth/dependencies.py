from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .service import AuthService
from .schemas import UserPermissionsDto

security_token = HTTPBearer()

async def check_token(auth: HTTPAuthorizationCredentials = Depends(security_token)) -> UserPermissionsDto:
    token = auth.credentials
    payload = AuthService.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    if not payload.active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return payload


async def check_admin(payload: UserPermissionsDto = Depends(check_token)) -> UserPermissionsDto:
    if not payload.is_admin:
        raise HTTPException(status_code=403, detail="Only for admins bro")
    return payload

async def check_manager(payload: UserPermissionsDto = Depends(check_token)) -> UserPermissionsDto:
    if not (payload.is_admin or payload.is_manager):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return payload