import io
import os

from PIL import Image
from bson import ObjectId

from fastapi import UploadFile, HTTPException

from app.abstracts import AbstractService
from app.autos import car_repo
from app.autos.auto_model import Pictures
from app.autos.schemas import CarCreate, CarUpdate
from app.core import settings


class FileService(AbstractService[CarCreate, CarUpdate]):
    def __init__(self):
        super().__init__(car_repo)

    SIZES = {
        "small": (300, 300),
        "large": (1200, 1200)
    }

    async def save_pict(self, car_id: str, picture: bytes ):

        try:
            image = Image.open(io.BytesIO(picture))
        except Exception:
            raise HTTPException(status_code=400, detail="Corrupted image")

        base_filename = f"{car_id}_img_"

        pictures = Pictures()

        for size_name, target_size in self.SIZES.items():
            img_copy = image.copy()
            img_copy.thumbnail(target_size, Image.Resampling.LANCZOS)
            final_path = os.path.join(settings.upload_dir, f"{base_filename}_{size_name}.webp")
            img_copy.save(final_path, format="WEBP", optimize=True, quality=80)
            setattr(pictures, size_name, final_path)
        upd = CarUpdate(
            img = pictures
        )
        res = await self.repo.update(ObjectId(car_id), upd)
        if not res:
            raise HTTPException(status_code=404, detail="Car not found")
        return res

