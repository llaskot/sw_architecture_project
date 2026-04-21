from fastapi import APIRouter, Response, Request, HTTPException
from pymongo.errors import DuplicateKeyError

from app.brands.schemas import BrandUpdate, BrandCreate
from app.brands.service import BrandService
from app.rents.schemas import RentCreate, RentRead, RentRequest
from app.rents.service import RentService

router = APIRouter(prefix="/rent", tags=["Rents"])

@router.post("/",
             )
async def create_rent(rent_data: RentRequest, response: Response):
    service = RentService()
    try:
        return await service.create(rent_data)
    except HTTPException as http_ex:
        raise http_ex
    except DuplicateKeyError as e:
        raise HTTPException(status_code=409, detail='DuplicateFieldError') from e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e)) from e
#
#
# @router.patch("/{brand_id}")
# async def update_brand(brand_id: str, brand_data: BrandUpdate, response: Response):
#     service = BrandService()
#     try:
#         return await service.update(brand_id, brand_data)
#     except HTTPException as http_ex:
#         raise http_ex
#     except DuplicateKeyError as e:
#         raise HTTPException(status_code=409, detail='DuplicateFieldError') from e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e)) from e
#
@router.get("/{rent_id}",
            response_model=RentRead
            )
async def get_by_id(rent_id: str):
    service = RentService()
    try:
        return await service.get_by_id(rent_id)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
#
@router.get("/")
async def get_all():
    service = RentService()
    try:
        return await service.get_all()
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
#
# @router.delete("/{brand_id}")
# async def delete(brand_id: str):
#     service = BrandService()
#     try:
#         return await service.delete(brand_id)
#     except HTTPException as http_ex:
#         raise http_ex
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e)) from e


