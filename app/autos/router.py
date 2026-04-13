from fastapi import APIRouter, Response, Request, HTTPException
from pymongo.errors import DuplicateKeyError

from app.autos import CarService
from app.autos.schemas import CarCreate, CarUpdate

#
router = APIRouter(prefix="/cars", tags=["Cars"])


@router.post("/")
async def create_car(car_data: CarCreate, response: Response):
    service = CarService()
    try:
        return await service.create(car_data)
    except HTTPException as http_ex:
        raise http_ex
    except DuplicateKeyError as e:
        raise HTTPException(status_code=409, detail='DuplicateFieldError') from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.patch("/{car_id}")
async def update_car(car_id: str, model_data: CarUpdate, response: Response):
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

@router.get("/")
async def get_all():
    service = CarService()
    try:
        return await service.get_all()
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.delete("/{car_id}")
async def delete(car_id: str):
    service = CarService()
    try:
        return await service.delete(car_id)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
