from fastapi import APIRouter, Response, Request, HTTPException, Depends
from pymongo.errors import DuplicateKeyError

from .checkup_model import CheckupModel
from .schemas import CheckupCreate, CheckupUpdate, CheckupRead, CheckupRequest
from .service import CheckupService
from app.auth import check_manager, check_admin, check_token
from app.users import UserPermissionsDto

router = APIRouter(prefix="/checkup", tags=["Checkup when returned"])


@router.post("/",  dependencies=[Depends(check_manager)])
async def create_checkup(checkup_data: CheckupRequest)  -> CheckupModel:
    service = CheckupService()
    try:
        create_dto = CheckupCreate(**checkup_data.model_dump())
        return await service.create(create_dto)
    except HTTPException as http_ex:
        raise http_ex
    except DuplicateKeyError as e:
        raise HTTPException(status_code=409, detail='DuplicateFieldError') from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.patch("/{checkup_id}", dependencies=[Depends(check_manager)])
async def checkup_model(checkup_id: str, checkup_data: CheckupUpdate) -> CheckupModel:
    service = CheckupService()
    try:
        return await service.update(checkup_id, checkup_data)
    except HTTPException as http_ex:
        raise http_ex
    except DuplicateKeyError as e:
        raise HTTPException(status_code=409, detail='DuplicateFieldError') from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/rent/{rent_id}")
async def get_by_rent_id(rent_id: str, user: UserPermissionsDto = Depends(check_token)) -> CheckupRead:
    service = CheckupService()
    try:
        return await service.get_checkup_by_rent(rent_id, user)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/{checkup_id}")
async def get_by_id(checkup_id: str, user: UserPermissionsDto = Depends(check_token)) -> CheckupRead:
    service = CheckupService()
    try:
        return await service.get_checkup(checkup_id, user)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e




@router.get("/", dependencies=[Depends(check_manager)])
async def get_all() -> list[CheckupRead]:
    service = CheckupService()
    try:
        return await service.get_all()
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
#
@router.delete("/{checkup_id}",  dependencies=[Depends(check_admin)])
async def delete(checkup_id: str):
    service = CheckupService()
    try:
        return await service.delete(checkup_id)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


