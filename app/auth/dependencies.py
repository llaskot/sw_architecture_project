from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.service import AuthService
from app.users import UserPermissionsDto

security_token = HTTPBearer()

async def check_token(auth: HTTPAuthorizationCredentials = Depends(security_token)) -> UserPermissionsDto:
    token = auth.credentials
    payload = AuthService.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    if not payload.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")
    return payload

