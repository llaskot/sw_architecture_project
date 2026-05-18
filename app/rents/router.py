from typing import Annotated, Optional

from fastapi import APIRouter, Response, Request, HTTPException, Depends, Query, Path
from pymongo.errors import DuplicateKeyError

from app.auth.dependencies import check_admin, check_token, check_manager
from app.auth.schemas import UserPermissionsDto
from app.autos.schemas import SortOrder
from app.brands.schemas import BrandUpdate, BrandCreate
from app.brands.service import BrandService
from app.rents.rent_model import RentStage
from app.rents.schemas import RentCreate, RentRead, RentRequest, RentUpdateRequest, ChangeStage
from app.rents.service import RentService

router = APIRouter(prefix="/rent", tags=["Rents"])


@router.post("/",
             )
async def create_rent(rent_data: RentRequest, user: UserPermissionsDto = Depends(check_token)):
    service = RentService()
    try:
        return await service.create_rent(rent_data, user)
    except HTTPException as http_ex:
        raise http_ex
    except DuplicateKeyError as e:
        raise HTTPException(status_code=409, detail='DuplicateFieldError') from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.patch("/{rent_id}")
async def update_rent(rent_id: str, rent_data: RentUpdateRequest, user: UserPermissionsDto = Depends(check_token)):
    service = RentService()
    try:
        return await service.update_rent(rent_id, rent_data, user)
    except HTTPException as http_ex:
        raise http_ex
    except DuplicateKeyError as e:
        raise HTTPException(status_code=409, detail='DuplicateFieldError') from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/{rent_id}",
            response_model=RentRead,
            )
async def get_by_id(rent_id: str, user: UserPermissionsDto = Depends(check_token)):
    service = RentService()
    try:
        return await service.get_rent(rent_id, user)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/")
async def get_all_rents(
        # hide_inactive: Annotated[bool, Query(
        #     description="For Admins only")] = True,

        stage: Annotated[
            Optional[list[RentStage]],
            Query(
                description="Multiple selection enabled. Hold **Ctrl** (Windows) or **Cmd** (Mac) to select several options.")
        ] = None,

        sort_date: SortOrder = SortOrder.DESC,
        page: int = 1,
        limit: int = 10,
        user: UserPermissionsDto = Depends(check_token)
        ):
    service = RentService()
    try:
        return await service.get_all_rents(stage, sort_date, page, limit, user)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/{rent_id}", dependencies=[Depends(check_admin)])
async def delete(rent_id: str):
    """
    Admin ONLY
    """
    service = RentService()
    try:
        return await service.delete_rent(rent_id)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.put("/{rent_id}/{stage}")
async def change_stage(rent_id: str,
                       stage: Annotated[RentStage, Path(description="Select stage")],
                       body: ChangeStage ,
                       user: UserPermissionsDto = Depends(check_manager)):
    """
    Admin or manager ONLY
    """
    service = RentService()
    try:
        return await service.change_stage(rent_id, stage, body, user)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
