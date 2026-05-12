from enum import Enum
from typing import Annotated, Optional

from fastapi import APIRouter, Response, Request, HTTPException, Depends, Query
from pymongo.errors import DuplicateKeyError

from app.auth.dependencies import check_admin
from app.auto_models.auto_model_model import CarCategory
from app.autos import CarService
from app.autos.schemas import CarCreate, CarUpdate, SortOrder, AllCarsResponse

#
router = APIRouter(prefix="/cars", tags=["Cars"])


@router.post("/", dependencies=[Depends(check_admin)])
async def create_car(car_data: CarCreate, response: Response):
    """
    Admin ONLY
    """
    service = CarService()
    try:
        return await service.create(car_data)
    except HTTPException as http_ex:
        raise http_ex
    except DuplicateKeyError as e:
        raise HTTPException(status_code=409, detail='DuplicateFieldError') from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.patch("/{car_id}", dependencies=[Depends(check_admin)])
async def update_car(car_id: str, model_data: CarUpdate, response: Response):
    """
    Admin ONLY
    """
    service = CarService()
    try:
        return await service.update(car_id, model_data)
    except HTTPException as http_ex:
        raise http_ex
    except DuplicateKeyError as e:
        raise HTTPException(status_code=409, detail='DuplicateFieldError') from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/{car_id}")
async def get_by_id(model_id: str):
    service = CarService()
    try:
        return await service.get_by_id(model_id)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


# @router.get("/")
# async def get_all():
#     service = CarService()
#     try:
#         return await service.get_all()
#     except HTTPException as http_ex:
#         raise http_ex
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e)) from e

@router.delete("/{car_id}", dependencies=[Depends(check_admin)])
async def delete(car_id: str):
    """
    Admin ONLY
    """
    service = CarService()
    try:
        return await service.delete(car_id)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/")
async def get_all(
        brand_ids: Annotated[Optional[list[str]], Query()] = None,
        # Список категорий
        categories: Annotated[
            Optional[list[CarCategory]],
            Query(
                description="Multiple selection enabled. Hold **Ctrl** (Windows) or **Cmd** (Mac) to select several options.")
        ] = None,
        search: Optional[str] = None,
        # Сортировки
        sort_price: SortOrder = SortOrder.DESC,
        sort_model: SortOrder = SortOrder.ASC,
        hide_inactive: Annotated[bool, Query(
            description="For Admins only")] = True,

        page: int = 1,
        limit: int = 10,
) -> AllCarsResponse:
    service = CarService()
    filters = {
        "brand_ids": brand_ids,
        "categories": categories,
        'search': search,
        "sort_price": sort_price,
        "sort_model": sort_model,
        "hide_inactive": hide_inactive,
        "page": page,
        "limit": limit,
    }
    try:
        return await service.get_all_set(filters)
    except HTTPException as http_ex:
        raise http_ex
    except IndexError :
        # raise HTTPException(status_code=404, detail=f"nothing found/ {str(e)}") from e
        res = {
            "total": 1,
            "page": 1,
            "limit": 10,
            "items": [],
        }
        return AllCarsResponse(**res)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
