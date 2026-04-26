from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.service import AuthService
from app.users.schemas import UserPermissionsDto

security_token = HTTPBearer()

async def check_token(auth: HTTPAuthorizationCredentials = Depends(security_token)) -> UserPermissionsDto:
    token = auth.credentials
    payload = AuthService.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    if not payload.active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return payload


async def check_admin(auth: HTTPAuthorizationCredentials = Depends(security_token)) -> UserPermissionsDto:
    payload = await check_token(auth)
    if not payload.is_admin:
        raise HTTPException(status_code=403, detail="Only for admins bro")
    return payload

async def check_manager(auth: HTTPAuthorizationCredentials = Depends(security_token)) -> UserPermissionsDto:
    payload = await check_token(auth)
    if not (payload.is_admin or payload.is_manager):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return payload