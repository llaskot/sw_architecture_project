from datetime import datetime

import pytest
from fastapi import HTTPException

from app.auth.schemas import  UserPermissionsDto
from app.rents.schemas import RentRequest, RentUpdateRequest

from tests.unit.auth.conftest import user_ent
from tests.unit.rents.conftest import rent_req_dto, car_model, rents_list, rent_ent,  payload, upd_rent


async def test_create_rent_success(
        rent_service,
        mock_rent_repo,
        mock_user_repo,
        mock_car_repo,
        dto: RentRequest = rent_req_dto,
        user_payload: UserPermissionsDto = payload):
    mock_car_repo.get_by_id.return_value = car_model
    mock_user_repo.get_by_id.return_value = user_ent
    mock_rent_repo.get_by_car_id.return_value = rents_list
    mock_rent_repo.create.return_value = rent_ent
    res = await rent_service.create_rent(dto, user_payload)
    assert res == rent_ent


async def test_create_rent_fail_date1(
        rent_service,
        mock_rent_repo,
        mock_user_repo,
        mock_car_repo,
        dto: RentRequest = rent_req_dto,
        user_payload: UserPermissionsDto = payload):
    mock_car_repo.get_by_id.return_value = car_model
    mock_user_repo.get_by_id.return_value = user_ent
    mock_rent_repo.get_by_car_id.return_value = rents_list
    mock_rent_repo.create.return_value = rent_ent
    dto.start_date = datetime.fromisoformat("2026-01-06T13:43:30.384Z")
    with pytest.raises(Exception) as exc_info:
        await rent_service.create_rent(dto, user_payload)
    assert exc_info.type == HTTPException
    assert exc_info.value.status_code == 409


async def test_create_rent_fail_date2(
        rent_service,
        mock_rent_repo,
        mock_user_repo,
        mock_car_repo,
        dto: RentRequest = rent_req_dto,
        user_payload: UserPermissionsDto = payload):
    mock_car_repo.get_by_id.return_value = car_model
    mock_user_repo.get_by_id.return_value = user_ent
    mock_rent_repo.get_by_car_id.return_value = rents_list
    mock_rent_repo.create.return_value = rent_ent
    dto.start_date = datetime.fromisoformat("2026-01-01T13:43:30.384Z")
    with pytest.raises(Exception) as exc_info:
        await rent_service.create_rent(dto, user_payload)
    assert exc_info.type == HTTPException
    assert exc_info.value.status_code == 409


async def test_create_rent_fail_date3(
        rent_service,
        mock_rent_repo,
        mock_user_repo,
        mock_car_repo,
        dto: RentRequest = rent_req_dto,
        user_payload: UserPermissionsDto = payload):
    mock_car_repo.get_by_id.return_value = car_model
    mock_user_repo.get_by_id.return_value = user_ent
    mock_rent_repo.get_by_car_id.return_value = rents_list
    mock_rent_repo.create.return_value = rent_ent
    dto.start_date = datetime.fromisoformat("2026-01-01T13:43:30.384Z")
    dto.days_qty = 3
    with pytest.raises(Exception) as exc_info:
        await rent_service.create_rent(dto, user_payload)
    assert exc_info.type == HTTPException
    assert exc_info.value.status_code == 409


async def test_create_rent_fail_date4(
        rent_service,
        mock_rent_repo,
        mock_user_repo,
        mock_car_repo,
        dto: RentRequest = rent_req_dto,
        user_payload: UserPermissionsDto = payload):
    mock_car_repo.get_by_id.return_value = car_model
    mock_user_repo.get_by_id.return_value = user_ent
    mock_rent_repo.get_by_car_id.return_value = rents_list
    mock_rent_repo.create.return_value = rent_ent
    dto.start_date = datetime.fromisoformat("2025-12-01T13:43:30.384Z")
    dto.days_qty = 35
    with pytest.raises(Exception) as exc_info:
        await rent_service.create_rent(dto, user_payload)
    assert exc_info.type == HTTPException
    assert exc_info.value.status_code == 409


async def test_create_rent_fail_date5(
        rent_service,
        mock_rent_repo,
        mock_user_repo,
        mock_car_repo,
        dto: RentRequest = rent_req_dto,
        user_payload: UserPermissionsDto = payload):
    mock_car_repo.get_by_id.return_value = car_model
    mock_user_repo.get_by_id.return_value = user_ent
    mock_rent_repo.get_by_car_id.return_value = rents_list
    mock_rent_repo.create.return_value = rent_ent
    dto.start_date = datetime.fromisoformat("2026-01-25T13:43:30.384Z")
    dto.days_qty = 1
    with pytest.raises(Exception) as exc_info:
        await rent_service.create_rent(dto, user_payload)
    assert exc_info.type == HTTPException
    assert exc_info.value.status_code == 409


async def test_update_rent_easy_success(
        rent_service,
        mock_rent_repo,
        mock_user_repo,
        mock_car_repo,
        rent_id="69eff1a595b371b221892943",
        body: dict = upd_rent,
        user_payload: UserPermissionsDto = payload):
    mock_car_repo.get_by_id.return_value = car_model
    mock_user_repo.get_by_id.return_value = user_ent
    mock_rent_repo.get_by_car_id.return_value = rents_list
    mock_rent_repo.update.return_value = True
    mock_rent_repo.get_by_id.return_value = rent_ent
    dto = RentUpdateRequest(
        **{k: v for k, v in body.items() if k not in ['start_date', 'days_qty', 'car_id']}
    )
    res = await rent_service.update_rent(rent_id, dto, user_payload)
    assert res == rent_ent

async def test_update_rent_car_success(
        rent_service,
        mock_rent_repo,
        mock_user_repo,
        mock_car_repo,
        rent_id="69eff1a595b371b221892943",
        body: dict = upd_rent,
        user_payload: UserPermissionsDto = payload):
    mock_car_repo.get_by_id.return_value = car_model
    mock_user_repo.get_by_id.return_value = user_ent
    mock_rent_repo.get_by_car_id.return_value = rents_list
    mock_rent_repo.update.return_value = True
    mock_rent_repo.get_by_id.return_value = rent_ent
    dto = RentUpdateRequest(
        **{k: v for k, v in body.items() if k not in ['start_date', 'days_qty']}
    )
    res = await rent_service.update_rent(rent_id, dto, user_payload)
    assert res == rent_ent

async def test_update_rent_car_term_success(
        rent_service,
        mock_rent_repo,
        mock_user_repo,
        mock_car_repo,
        rent_id="69eff1a595b371b221892943",
        body: dict = upd_rent,
        user_payload: UserPermissionsDto = payload):
    mock_car_repo.get_by_id.return_value = car_model
    mock_user_repo.get_by_id.return_value = user_ent
    mock_rent_repo.get_by_car_id.return_value = rents_list
    mock_rent_repo.update.return_value = True
    mock_rent_repo.get_by_id.return_value = rent_ent
    dto = RentUpdateRequest(
        **{k: v for k, v in body.items() if k not in ['start_date']}
    )
    dto.days_qty = 150
    res = await rent_service.update_rent(rent_id, dto, user_payload)
    assert res == rent_ent

async def test_update_rent_full_success(
        rent_service,
        mock_rent_repo,
        mock_user_repo,
        mock_car_repo,
        rent_id="69eff1a595b371b221892943",
        body: dict = upd_rent,
        user_payload: UserPermissionsDto = payload):
    mock_car_repo.get_by_id.return_value = car_model
    mock_user_repo.get_by_id.return_value = user_ent
    mock_rent_repo.get_by_car_id.return_value = rents_list
    mock_rent_repo.update.return_value = True
    mock_rent_repo.get_by_id.return_value = rent_ent
    dto = RentUpdateRequest(
        **body
    )
    dto.days_qty = 150
    dto.start_date = datetime.fromisoformat("2026-01-09T13:43:30.384Z")
    res = await rent_service.update_rent(rent_id, dto, user_payload)
    assert res == rent_ent

async def test_update_rent_date_fail(
        rent_service,
        mock_rent_repo,
        mock_user_repo,
        mock_car_repo,
        rent_id="69eff1a595b371b221892943",
        body: dict = upd_rent,
        user_payload: UserPermissionsDto = payload):
    mock_car_repo.get_by_id.return_value = car_model
    mock_user_repo.get_by_id.return_value = user_ent
    mock_rent_repo.get_by_car_id.return_value = rents_list
    mock_rent_repo.update.return_value = True
    mock_rent_repo.get_by_id.return_value = rent_ent
    dto = RentUpdateRequest(
        **body
    )
    dto.start_date = datetime.fromisoformat("2026-01-06T13:43:30.384Z")
    with pytest.raises(Exception) as exc_info:
        await rent_service.update_rent(rent_id, dto, user_payload)
    assert exc_info.type == HTTPException
    assert exc_info.value.status_code == 409
    print(exc_info.value)

async def test_update_rent_date_fail2(
        rent_service,
        mock_rent_repo,
        mock_user_repo,
        mock_car_repo,
        rent_id="69eff1a595b371b221892943",
        body: dict = upd_rent,
        user_payload: UserPermissionsDto = payload):
    mock_car_repo.get_by_id.return_value = car_model
    mock_user_repo.get_by_id.return_value = user_ent
    mock_rent_repo.get_by_car_id.return_value = rents_list
    mock_rent_repo.update.return_value = True
    mock_rent_repo.get_by_id.return_value = rent_ent
    dto = RentUpdateRequest(
        **body
    )
    dto.start_date = datetime.fromisoformat("2026-01-01T13:43:30.384Z")
    dto.days_qty = 3
    with pytest.raises(Exception) as exc_info:
        await rent_service.update_rent(rent_id, dto, user_payload)
    assert exc_info.type == HTTPException
    assert exc_info.value.status_code == 409
    print(exc_info.value)