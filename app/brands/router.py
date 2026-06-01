from fastapi import APIRouter, Response, HTTPException, Depends
from pymongo.errors import DuplicateKeyError

from .schemas import BrandUpdate, BrandCreate
from .service import BrandService
from app.auth import check_admin, check_manager
from app.users import UserPermissionsDto

router = APIRouter(prefix="/brand", tags=["Brands"])


@router.get("/admin/")
async def get_all_admin(hide_inactive: bool = True, user: UserPermissionsDto = Depends(check_manager)):
    service = BrandService()
    try:
        return await service.get_all(hide_inactive if user.is_admin else True)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/admin/{brand_id}")
async def get_by_id(brand_id: str, user: UserPermissionsDto = Depends(check_manager)):
    service = BrandService()
    try:
        return await service.get_by_id(brand_id, False if user.is_admin else True)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/",  dependencies=[Depends(check_admin)])
async def create_brand(brand_data: BrandCreate, response: Response):
    """
    Admin ONLY
    """
    service = BrandService()
    try:
        return await service.create(brand_data)
    except HTTPException as http_ex:
        raise http_ex
    except DuplicateKeyError as e:
        raise HTTPException(status_code=409, detail='DuplicateFieldError') from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
#
#
@router.patch("/{brand_id}",  dependencies=[Depends(check_admin)])
async def update_brand(brand_id: str, brand_data: BrandUpdate, response: Response):
    """
    Admin ONLY
    """
    service = BrandService()
    try:
        return await service.update(brand_id, brand_data)
    except HTTPException as http_ex:
        raise http_ex
    except DuplicateKeyError as e:
        raise HTTPException(status_code=409, detail='DuplicateFieldError') from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/{brand_id}")
async def get_by_id(brand_id: str):
    service = BrandService()
    try:
        return await service.get_by_id(brand_id)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/")
async def get_all():
    service = BrandService()
    try:
        return await service.get_all()
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.delete("/{brand_id}",  dependencies=[Depends(check_admin)])
async def delete(brand_id: str):
    """
    Admin ONLY
    """
    service = BrandService()
    try:
        return await service.delete(brand_id)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


