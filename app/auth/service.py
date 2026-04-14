import json
import base64
import hashlib
import os
import secrets
import time
from typing import Final

import bcrypt
import jwt
from bson import ObjectId
from cryptography.fernet import Fernet
from fastapi import HTTPException, Response

from app.auth.schemas import ConfirmationCode, LoginDto
from app.users.repository import user_repo
from app.users.schemas import UserRegistrate, UserCreate, UserPermissionsDto
from app.users.user_model import User

class AuthService:
    def __init__(self):
        self._generated_key = None

    ENV_PASSPHRASE: Final = os.getenv("SECRET_KEY")
    REFRESH_AGE: Final = 48 * 60 * 60

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

    def _encrypt_registration_data(self, user_data: UserRegistrate, code: str) -> str:
        # Конвертируем DTO в обычный словарь
        user_dict = user_data.model_dump()
        payload = {
            "user": user_dict,
            "code": code
        }
        code_key = self._get_generated_key()
        return code_key.encrypt(json.dumps(payload).encode()).decode()

    def _decrypt_registration_data(self, encrypted_data: str) -> tuple[UserCreate, str]:
        code_key = self._get_generated_key()
        decrypted_bytes = code_key.decrypt(encrypted_data.encode())
        decrypted_json = decrypted_bytes.decode()
        payload = json.loads(decrypted_json)

        # 4. Восстанавливаем DTO и код
        # Pydantic сам разложит словарь обратно в модель
        user_data = UserCreate(**payload["user"])
        code = payload["code"]
        return user_data, code

    #
    def _generate_verification_code(self) -> str:
        # generate confirm code 100 000 - 999 999
        return str(secrets.randbelow(900000) + 100000)

    #
    def register_new_user(self, user_data: UserRegistrate):
        confirm_code = self._generate_verification_code()
        encoded_user = self._encrypt_registration_data(user_data, confirm_code)

        # HERE WILL BEE MAILER

        return confirm_code, encoded_user

    async def create_user(self, conf_code: ConfirmationCode, encoded_user: str):
        user_dto, code = self._decrypt_registration_data(encoded_user)
        if conf_code.conf_code != code:
            raise HTTPException(
                status_code=400,
                detail=f"incorrect confirmation code"
            )
        user_dto.password = self.get_password_hash(user_dto.password)
        return await user_repo.create(user_dto)

    def create_token(self, payload: dict):
        key = os.getenv("JWT_SOLT")
        payload["exp"] = int(time.time()) + (10 * 60)
        access = jwt.encode(payload, key, algorithm="HS256")
        payload["exp"] = int(time.time()) + AuthService.REFRESH_AGE
        refresh = jwt.encode(payload, key, algorithm="HS256")
        return {"access_token": access, "refresh_token": refresh}

    def decode_token(self, token: str) -> UserPermissionsDto | None:
        key = os.getenv("JWT_SOLT")
        try:
            payload = jwt.decode(token, key, algorithms=["HS256"])
            return UserPermissionsDto.model_validate(payload)
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    async def refresh(self, refresh_token: str):
        payload = self.decode_token(refresh_token)
        if payload is None:
            raise HTTPException(status_code=400, detail="Invalid refresh token")
        return await user_repo.get_by_id(ObjectId(payload.id))

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
        user = User.model_validate(await user_repo.find_for_logining(data))
        if not user or not self.verify_password(data.password, user.password):
            raise HTTPException(
                status_code=403,
                detail="Incorrect username or password"
            )
        return user

    def prepare_tokens(self, user: User, response: Response):
        permissions = UserPermissionsDto.model_validate(user)
        user_payload = permissions.model_dump()
        tokens = self.create_token(user_payload)
        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh_token"],
            httponly=True,
            samesite="lax",
            path="/auth/refresh",
            max_age=self.REFRESH_AGE
        )
        return tokens["access_token"]
#
