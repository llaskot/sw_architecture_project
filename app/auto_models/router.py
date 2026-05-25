# from beanie import PydanticObjectId
from bson import ObjectId
from fastapi import APIRouter, Response, Request, HTTPException, Depends
from pymongo.errors import DuplicateKeyError

from app.auth.dependencies import check_admin, check_manager
from app.auth.schemas import UserPermissionsDto
#
from app.auto_models.schemas import AutoModelCreate, AutoModelUpdate
from app.auto_models.service import AutoModelService

#
#
router = APIRouter(prefix="/models", tags=["Auto Model"])


@router.get("/categories")
async def get_categories():
    service = AutoModelService()
    try:
        return await service.get_categories()
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/admin")

async def get_all_admin(hide_inactive: bool = True, user: UserPermissionsDto = Depends(check_manager)):
    service = AutoModelService()

    try:
        return await service.get_all(hide_inactive if user.is_admin else True)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/", dependencies=[Depends(check_admin)])
async def create_model(model_data: AutoModelCreate, response: Response):
    """
    Admin ONLY
    """
    service = AutoModelService()
    try:
        return await service.create(model_data)
    except HTTPException as http_ex:
        raise http_ex
    except DuplicateKeyError as e:
        raise HTTPException(status_code=409, detail='DuplicateFieldError') from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


#
#
@router.patch("/{model_id}", dependencies=[Depends(check_admin)])
async def update_model(model_id: str, model_data: AutoModelUpdate, response: Response):
    """
    Admin ONLY
    """
    service = AutoModelService()
    try:
        return await service.update(model_id, model_data)
    except HTTPException as http_ex:
        raise http_ex
    except DuplicateKeyError as e:
        raise HTTPException(status_code=409, detail='DuplicateFieldError') from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


#
@router.get("/{model_id}")
async def get_by_id(model_id: str):
    service = AutoModelService()
    try:
        return await service.get_by_id(model_id)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/admin/{model_id}")
async def get_by_id_adm(model_id: str,
                     user: UserPermissionsDto = Depends(check_manager)):
    service = AutoModelService()
    try:
        return await service.get_by_id(model_id, False if user.is_admin else True)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/")
async def get_all():
    service = AutoModelService()
    try:
        return await service.get_all()
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/{model_id}", dependencies=[Depends(check_admin)])
async def delete(model_id: str,):
    """
    Admin ONLY
    """
    service = AutoModelService()
    try:
        return await service.delete(model_id)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
