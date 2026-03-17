from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException

from app.users.schemas import UserCreate, UserOut
from app.users.service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def get_users():
    return [{"username": "hacker grandma"}]

@router.post("/",  response_model=UserOut)
async def create_users(user_data: UserCreate):
    return await UserService.register_new_user(user_data)


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: PydanticObjectId):

    return await UserService.get_user_by_id(user_id)



