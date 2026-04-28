# from beanie import PydanticObjectId
from bson import ObjectId
from fastapi import APIRouter, Response, Request, HTTPException, Depends
from pymongo.errors import DuplicateKeyError

from app.auth.dependencies import check_manager, check_admin
#
from app.auto_models.schemas import AutoModelCreate, AutoModelUpdate, AutoModelRead
from app.auto_models.service import AutoModelService
from app.checkup.checkup_model import CheckupModel
from app.checkup.schemas import CheckupCreate, CheckupUpdate, CheckupRead
from app.checkup.service import CheckupService

#
#
router = APIRouter(prefix="/checkup", tags=["Checkup when returned"])




@router.post("/",  dependencies=[Depends(check_manager)])
async def create_checkup(checkup_data: CheckupCreate)  -> CheckupModel:
    service = CheckupService()
    try:
        return await service.create(checkup_data)
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
#
@router.get("/{checkup_id}")
async def get_by_id(checkup_id: str) -> CheckupRead:
    service = CheckupService()
    try:
        return await service.get_by_id(checkup_id)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/")
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


