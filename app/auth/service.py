import json
import base64
import hashlib
import secrets
import time
from typing import Final

import bcrypt
import jwt
from bson import ObjectId
from cryptography.fernet import Fernet
from fastapi import HTTPException, Response

from .schemas import ConfirmationCode, PassRestore, ChangePassword
from app.users import UserRegistrate, UserCreate, User, LoginDto, UserPermissionsDto
from app.core import settings
from app.users import user_repo as us_repo



class AuthService:
    def __init__(self, user_repo = us_repo):
        self._user_repo = user_repo
        self._generated_key = None

    ENV_PASSPHRASE: Final = settings.secret_key
    REFRESH_AGE: Final = 24 * 60 * 60
    ACCESS_AGE: Final = 10 * 60

    # REFRESH_AGE: Final = 3 * 60
    # ACCESS_AGE: Final = 1 * 60


    #
    def _get_generated_key(self):
        if self._generated_key is None:
            passphrase = self.ENV_PASSPHRASE
            if not passphrase:
                raise ValueError("AUTH_SECRET_KEY not found in environment variables")
            key_hash = hashlib.sha256(passphrase.encode()).digest()
            fernet_key = base64.urlsafe_b64encode(key_hash)
            self._generated_key = Fernet(fernet_key)
        return self._generated_key

    def _encrypt_registration_data(self, user_data: UserRegistrate | dict, code: str) -> str:
        if isinstance(user_data, UserRegistrate):
            user_dict = user_data.model_dump()
        else:
            user_dict = user_data
        payload = {
            "user": user_dict,
            "code": code
        }
        code_key = self._get_generated_key()
        return code_key.encrypt(json.dumps(payload).encode()).decode()

    def _decrypt_registration_data(self, encrypted_data: str) -> tuple[UserCreate, str]:
        payload = self._decrypt(encrypted_data)
        user_data = UserCreate(**payload["user"])
        code = payload["code"]
        return user_data, code


    def _decrypt(self, encrypted_data: str) -> dict:
        code_key = self._get_generated_key()
        decrypted_bytes = code_key.decrypt(encrypted_data.encode())
        decrypted_json = decrypted_bytes.decode()
        return json.loads(decrypted_json)

    #
    def _generate_verification_code(self) -> str:
        return str(secrets.randbelow(900000) + 100000)

    #
    def register_new_user(self, user_data: UserRegistrate):
        confirm_code = self._generate_verification_code()
        encoded_user = self._encrypt_registration_data(user_data, confirm_code)
        return confirm_code, encoded_user

    async def create_user(self, conf_code: ConfirmationCode, encoded_user: str):
        user_dto, code = self._decrypt_registration_data(encoded_user)
        if conf_code.conf_code != code:
            raise HTTPException(
                status_code=401,
                detail=f"incorrect confirmation code"
            )
        user_dto.password = self.get_password_hash(user_dto.password)
        return await self._user_repo.create(user_dto)

    def create_token(self, payload: dict):
        key = settings.jwt_solt
        payload["exp"] = int(time.time()) + AuthService.ACCESS_AGE
        access = jwt.encode(payload, key, algorithm="HS256")
        payload["exp"] = int(time.time()) + AuthService.REFRESH_AGE
        refresh = jwt.encode(payload, key, algorithm="HS256")
        return {"access_token": access, "refresh_token": refresh}

    @staticmethod
    def decode_token(token: str) -> UserPermissionsDto | None:
        key = settings.jwt_solt
        try:
            payload = jwt.decode(token, key, algorithms=["HS256"])
            res = UserPermissionsDto.model_validate(payload)
            return res
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    async def refresh(self, refresh_token: str):
        payload: UserPermissionsDto = self.decode_token(refresh_token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        res = await self._user_repo.get_by_id(ObjectId(payload.id))
        return res

    def get_password_hash(self, password: str) -> str:
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(pwd_bytes, salt)
        return hashed_password.decode('utf-8')

    def verify_password(self, input_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            input_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )


    async def login_user(self, data: LoginDto) -> User:
        res_success = await self._user_repo.find_for_logining(data)
        if not res_success:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password"
            )
        user = User.model_validate(res_success)
        if not user or not self.verify_password(data.password, user.password):
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password"
            )
        return user

    def prepare_tokens(self, user: User, response: Response):
        permissions = UserPermissionsDto.model_validate(user)
        user_payload = permissions.model_dump(mode="json")
        tokens = self.create_token(user_payload)
        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh_token"],
            httponly=True,
            samesite="lax",
            path= settings.vite_api_url+"/auth/refresh",
            max_age=self.REFRESH_AGE
        )
        return tokens["access_token"]


    async def get_restore_code(self, restore_dto: PassRestore):
        res_success = await self._user_repo.find_for_logining(restore_dto)
        if not res_success:
            raise HTTPException(
                status_code=401,
                detail="Incorrect credentials"
            )
        id = str(res_success.get("_id"))
        code = self._generate_verification_code()
        encoded_user = self._encrypt_registration_data({"id": id}, code)
        return res_success.get("email"), code, encoded_user

    async def change_password(self, body: ChangePassword, encoded_user: str):
        decrypted = self._decrypt(encoded_user)
        if decrypted['code'] != body.conf_code:
            raise HTTPException(
                status_code=400,
                detail=f"incorrect confirmation code"
            )
        await self._user_repo.change_password(decrypted["user"]["id"], self.get_password_hash(body.new_password))
        return {"success": True, "message": "Password changed successfully"}
