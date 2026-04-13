from app.abstracts import AbstractService
from app.autos.repository import car_repo
from app.autos.schemas import CarCreate, CarUpdate


class CarService(AbstractService[CarCreate, CarUpdate]):
    def __init__(self):
        super().__init__(car_repo)