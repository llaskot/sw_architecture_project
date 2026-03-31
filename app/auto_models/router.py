from beanie import PydanticObjectId
from fastapi import APIRouter, Response, Request, HTTPException

from app.brands import Brand
from app.brands.schemas import BrandCreate, BrandUpdate
from app.brands.service import BrandService

# def get_brand_service():
#     return BrandService()

router = APIRouter(prefix="/brand", tags=["Brand"])

@router.post("/")
async def create_brand(brand_data: BrandCreate, response: Response):
    service = BrandService()
    try:
        return await service.create(brand_data)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.patch("/{brand_id}")
async def update_brand(brand_id: PydanticObjectId, brand_data: BrandUpdate, response: Response):
    service = BrandService()
    try:
        return await service.update(brand_id, brand_data)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/{brand_id}")
async def get_by_id(brand_id: PydanticObjectId):
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

@router.delete("/{brand_id}")
async def delete(brand_id: PydanticObjectId):
    service = BrandService()
    try:
        return await service.delete(brand_id)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
