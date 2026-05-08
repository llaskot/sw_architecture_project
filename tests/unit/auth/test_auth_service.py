import pytest
from fastapi import HTTPException
from pydantic_mongo import ObjectIdField

from app.auth.schemas import ConfirmationCode, UserPermissionsDto, LoginDto
from app.users.schemas import UserRegistrate

request_dto = UserRegistrate(
    email="test@email.com",
    login="testlogin",
    password="password",
    first_name="wasya",
    last_name="Pupkin"
)

payload = UserPermissionsDto(
    id=ObjectIdField('69eff1a495b371b221892935'),
    active=True,
    is_admin=False,
    is_manager=False)

login_dto = LoginDto(
    login="User_test",
    password="String11")

login_dto2 = LoginDto(
    login="user_test@example.com",
    password="String11")

def test_register_new_user(auth_service, reg_dto=request_dto):
    confirm_code, encoded_user = auth_service.register_new_user(reg_dto)
    assert isinstance(confirm_code, str)
    assert len(confirm_code) == 6
    decr_data = auth_service._decrypt(encoded_user)
    assert isinstance(decr_data, dict)
    assert decr_data['user']['email'] == reg_dto.email
    assert decr_data['user']['login'] == reg_dto.login
    assert decr_data['user']['first_name'] == reg_dto.first_name
    assert decr_data['user']['last_name'] == reg_dto.last_name
    assert decr_data['user']['password'] == reg_dto.password
    assert decr_data["code"] == confirm_code


async def test_create_user_success(auth_service, reg_dto=request_dto):
    encr_data = auth_service._encrypt_registration_data(reg_dto, "111111")
    cc = ConfirmationCode(
        conf_code="111111"
    )
    result = await auth_service.create_user(cc, encr_data)
    assert result.email == reg_dto.email
    assert result.login == reg_dto.login
    assert result.first_name == reg_dto.first_name
    assert result.last_name == reg_dto.last_name
    assert result.password != reg_dto.password
    assert result.password.startswith("$2b$")


async def test_create_user_wrong_code(auth_service, reg_dto=request_dto):
    encr_data = auth_service._encrypt_registration_data(reg_dto, "111111")
    cc = ConfirmationCode(
        conf_code="111112"
    )
    with pytest.raises(Exception) as exc_info:
        await auth_service.create_user(cc, encr_data)
    assert exc_info.type == HTTPException
    assert exc_info.value.status_code == 401


async def test_refresh_success(auth_service, pll=payload):
    d = pll.model_dump()
    d["id"] = str(d["id"])
    tokens = auth_service.create_token(d)
    print("AAAAAA",len(tokens["access_token"]))
    res = await auth_service.refresh(tokens["access_token"])
    assert res == pll.id

async def test_refresh_fail(auth_service, pll=payload):
    d = pll.model_dump()
    d["id"] = str(d["id"])
    tokens = auth_service.create_token(d)
    tokens["access_token"] = tokens["access_token"][:200]+"AAAAAAAAAAAAAAA"
    with pytest.raises(Exception) as exc_info:
        await auth_service.refresh(tokens["access_token"])
    assert exc_info.type == HTTPException
    assert exc_info.value.status_code == 401


async def test_login_user_login_success(auth_service, creds=login_dto):
    res = await auth_service.login_user(creds)
    assert res.login == creds.login

async def test_login_user_email_success(auth_service, creds=login_dto2):
    res = await auth_service.login_user(creds)
    assert res.email == creds.login

async def test_login_user_invalid_password(auth_service, creds=login_dto2):
    creds.password = creds.password + "1"
    with pytest.raises(Exception) as exc_info:
        await auth_service.login_user(creds)
    assert exc_info.type == HTTPException
    assert exc_info.value.status_code == 401


async def test_login_user_invalid_login(auth_service, mock_user_repo, creds=login_dto):
    mock_user_repo.find_for_logining.return_value = None
    with pytest.raises(Exception) as exc_info:
        await auth_service.login_user(creds)
    assert exc_info.type == HTTPException
    assert exc_info.value.status_code == 401



