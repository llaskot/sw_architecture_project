from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Depends
from pymongo.errors import PyMongoError

from app.auth.dependencies import check_token
from app.users import UserPermissionsDto
from app.users.schemas import UserCreate, UserResponse, UserResponseBasic
from app.users.service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def get_users():
    return [{"username": "hacker grandma"}]


# @router.post("/", response_model=UserResponse)
# async def create_users(user_data: UserCreate):
#     return await UserService.register_new_user(user_data)

@router.get("/profile", response_model=UserResponse)
async def get_profile(user: UserPermissionsDto = Depends(check_token)):
    try:
        return await UserService.get_user_by_id(PydanticObjectId(user.id))
    except HTTPException as e:
        raise e from e
    except Exception as e:
        if isinstance(e, PyMongoError):
            raise HTTPException(status_code=500, detail=f"Database error:\n {str(e)}") from e
        raise HTTPException(status_code=500, detail=f"Server error: \n{str(e)}") from e


@router.get("/{user_id}", response_model=UserResponseBasic)
async def get_user(user_id: PydanticObjectId):
    try:
        return await UserService.get_user_by_id(user_id)
    except HTTPException as e:
        raise e from e
    except Exception as e:
        if isinstance(e, PyMongoError):
            raise HTTPException(status_code=500, detail=f"Database error:\n {str(e)}") from e
        raise HTTPException(status_code=500, detail=f"Server error: \n{str(e)}") from e
