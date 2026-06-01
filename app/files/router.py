from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pymongo.errors import DuplicateKeyError

from .service import FileService
from app.auth import check_admin

router = APIRouter(prefix="/files", tags=["Files"])

@router.post("/{car_id}",  dependencies=[Depends(check_admin)])
async def save_pict(car_id: str, file: UploadFile = File(...)):
    """
    Admin ONLY
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="File must be an image"
        )
    service = FileService()
    try:
        image_bytes = await file.read()
        res = await  service.save_pict(car_id, image_bytes)
        return  res
    except HTTPException as http_ex:
        raise http_ex
    except DuplicateKeyError as e:
        raise HTTPException(status_code=409, detail='DuplicateFieldError') from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e