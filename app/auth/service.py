import json
import base64
import hashlib
import os
import secrets
import time
from typing import Final

import bcrypt
import jwt
from beanie import PydanticObjectId
from cryptography.fernet import Fernet
from fastapi import HTTPException, Response

from app.auth.schemas import ConfirmationCode, LoginDto
from app.users import UserCreate, User, get_user_by_id, user_repo, UserPermissionsDto


class AuthService:
    _generated_key = None
    ENV_PASSPHRASE: Final = os.getenv("SECRET_KEY")
    REFRESH_AGE: Final = 48 * 60 * 60

    @classmethod
    def _get_generated_key(cls):
        if cls._generated_key is None:
            passphrase = cls.ENV_PASSPHRASE
            if not passphrase:
                raise ValueError("AUTH_SECRET_KEY not found in environment variables")
            key_hash = hashlib.sha256(passphrase.encode()).digest()
            fernet_key = base64.urlsafe_b64encode(key_hash)
            cls._generated_key = Fernet(fernet_key)
        return cls._generated_key

    @classmethod
    def _encrypt_registration_data(cls, user_data: UserCreate, code: str) -> str:
        # Конвертируем DTO в обычный словарь
        user_dict = user_data.model_dump()
        payload = {
            "user": user_dict,
            "code": code
        }
        code_key = cls._get_generated_key()
        return code_key.encrypt(json.dumps(payload).encode()).decode()

    @classmethod
    def _decrypt_registration_data(cls, encrypted_data: str) -> tuple[UserCreate, str]:
        code_key = cls._get_generated_key()

        decrypted_bytes = code_key.decrypt(encrypted_data.encode())
        decrypted_json = decrypted_bytes.decode()

        payload = json.loads(decrypted_json)

        # 4. Восстанавливаем DTO и код
        # Pydantic сам разложит словарь обратно в модель
        user_data = UserCreate(**payload["user"])
        code = payload["code"]

        return user_data, code

    @staticmethod
    def _generate_verification_code() -> str:
        # generate confirm code 100 000 - 999 999
        return str(secrets.randbelow(900000) + 100000)

    @staticmethod
    def register_new_user(user_data: UserCreate):
        confirm_code = AuthService._generate_verification_code()
        encoded_user = AuthService._encrypt_registration_data(user_data, confirm_code)

        # HERE WILL BEE MAILER

        return confirm_code, encoded_user

    @staticmethod
    async def create_user(conf_code: ConfirmationCode, encoded_user: str):
        user_dto, code = AuthService._decrypt_registration_data(encoded_user)
        if conf_code.conf_code != code:
            raise HTTPException(
                status_code=400,
                detail=f"incorrect confirmation code"
            )
        user_dto.password = AuthService.get_password_hash(user_dto.password)
        return await user_repo.save_user(user_dto)

    @staticmethod
    def create_token(payload: dict):
        key = os.getenv("JWT_SOLT")
        payload["exp"] = int(time.time()) + (10 * 60)
        access = jwt.encode(payload, key, algorithm="HS256")
        payload["exp"] = int(time.time()) + AuthService.REFRESH_AGE
        refresh = jwt.encode(payload, key, algorithm="HS256")
        return {"access_token": access, "refresh_token": refresh}

    @staticmethod
    def decode_token(token: str) -> UserPermissionsDto | None:
        key = os.getenv("JWT_SOLT")
        try:
            payload = jwt.decode(token, key, algorithms=["HS256"])
            return UserPermissionsDto.model_validate(payload)
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    async def refresh(refresh_token: str):
        payload = AuthService.decode_token(refresh_token)

        if payload is None:
            raise HTTPException(status_code=400, detail="Invalid refresh token")
        return await get_user_by_id(PydanticObjectId(payload.id))

    @staticmethod
    def get_password_hash(password: str) -> str:
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(pwd_bytes, salt)
        return hashed_password.decode('utf-8')

    @staticmethod
    def verify_password(input_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            input_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )

    @staticmethod
    async def login_user(data: LoginDto) -> User:
        user = await user_repo.find_for_logining(data)
        if not user or not AuthService.verify_password(data.password, user.password):
            raise HTTPException(
                status_code=403,
                detail="Incorrect username or password"
            )
        return user

    @staticmethod
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
            max_age=AuthService.REFRESH_AGE
        )
        return tokens["access_token"]


