from app.abstracts import AbstractService
from app.brands import brand_repo
from app.brands.schemas import BrandCreate, BrandUpdate


class BrandService(AbstractService[BrandCreate, BrandUpdate]):
    def __init__(self):
        super().__init__(brand_repo)