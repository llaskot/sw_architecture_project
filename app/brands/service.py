from .repository import brand_repo
from .schemas import BrandCreate, BrandUpdate
from app.abstracts import AbstractService


class BrandService(AbstractService[BrandCreate, BrandUpdate]):
    def __init__(self):
        super().__init__(brand_repo)