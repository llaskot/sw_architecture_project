from typing import Optional, Annotated

from fastapi import APIRouter, HTTPException, Depends, Query
from pymongo.errors import DuplicateKeyError, PyMongoError

from .schemas import UserCreate, UserResponseAdm, UserUpdate, UserUpdateShort, AllUsersResponse
from .service import UserService
from ..auth.dependencies import check_admin, check_manager, check_token
from ..auth.schemas import UserPermissionsDto
from ..autos.schemas import SortOrder

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponseAdm, dependencies=[Depends(check_admin)])
async def create_user(user_data: UserCreate):
    """
    Admin only
    """
    service = UserService()
    try:
        return await service.create(user_data)
    except HTTPException as http_ex:
        raise http_ex
    except DuplicateKeyError as e:
        raise HTTPException(status_code=409, detail=f"Duplicate value for field: {e.details['keyPattern']}") from e
    except Exception as e:
        # print(e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/profile", response_model=UserResponseAdm)
async def get_profile(user: UserPermissionsDto = Depends(check_token)):
    """
    Owner only
    """
    service = UserService()
    try:
        return await service.get_by_id(user.id)
    except HTTPException as e:
        raise e from e
    except Exception as e:
        if isinstance(e, PyMongoError):
            raise HTTPException(status_code=500, detail=f"Database error:\n {str(e)}") from e
        raise HTTPException(status_code=500, detail=f"Server error: \n{str(e)}") from e



@router.get("/{user_id}", response_model=UserResponseAdm, dependencies=[Depends(check_manager)])
async def get_user(user_id: str):
    """
    Manager or Admin only
    """
    service = UserService()
    try:
        return await service.get_by_id(user_id)
    except HTTPException as e:
        raise e from e
    except Exception as e:
        if isinstance(e, PyMongoError):
            raise HTTPException(status_code=500, detail=f"Database error:\n {str(e)}") from e
        raise HTTPException(status_code=500, detail=f"Server error: \n{str(e)}") from e


@router.get("/", response_model=AllUsersResponse)
async def get_all(
        search: Optional[str] = None,
        hide_inactive: Annotated[bool, Query(
            description="For Admins only")] = False,
        page: int = 1,
        limit: int = 10,
        user: UserPermissionsDto = Depends(check_manager)
) -> AllUsersResponse:
    """
    Manager only
    """
    service = UserService()
    try:
        return await service.get_all_search(search, hide_inactive, page, limit, user)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e





@router.patch("/profile", response_model=UserResponseAdm)
async def update_profile(user_data: UserUpdateShort, user: UserPermissionsDto = Depends(check_token)):
    """
    Owner only
    """
    service = UserService()
    try:
        return await service.update(user.id, UserUpdate(**user_data.model_dump(exclude_unset=True)))
    except HTTPException as http_ex:
        raise http_ex
    except DuplicateKeyError as e:
        raise HTTPException(status_code=409, detail=f"Duplicate value for field: {e.details['keyPattern']}") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e





@router.patch("/{user_id}", response_model=UserResponseAdm, dependencies=[Depends(check_manager)])
async def update_user(user_id: str, user_data: UserUpdate):
    """
    Admin only
    """
    service = UserService()
    try:
        return await service.update(user_id, user_data)
    except HTTPException as http_ex:
        raise http_ex
    except DuplicateKeyError as e:
        raise HTTPException(status_code=409, detail=f"Duplicate value for field: {e.details['keyPattern']}") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/{user_id}", dependencies=[Depends(check_admin)])
async def delete(user_id: str):
    """
    Admin only
    """
    service = UserService()
    try:
        return await service.delete(user_id)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
