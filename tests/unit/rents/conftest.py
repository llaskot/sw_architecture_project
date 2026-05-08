from unittest.mock import AsyncMock

import pytest
from pydantic_mongo import ObjectIdField

from app.auth.schemas import UserPermissionsDto
from app.autos.schemas import CarRead
from app.rents.schemas import RentRequest, RentRead, RentUpdateRequest
from app.rents.service import RentService
from app.users.user_model import User

payload = UserPermissionsDto(
    id=ObjectIdField('69fae74679ac4be5cc062826'),
    active=True,
    is_admin=False,
    is_manager=False)

rent_req = {
    "car_id": "69eff1a695b371b221892947",
    "driver": False,
    "user_dock": "69eff1a495b371b221892935",
    "start_date": "2026-01-10T13:43:30.384Z",
    "days_qty": 10
}

rent_req_dto = RentRequest(
    **rent_req
)

upd_rent = {
  "car_id": "69eff1a695b371b221892947",
  "driver": True,
  "user_dock": "string",
  "start_date": "2026-05-06T17:45:53.676Z",
  "days_qty": 1
}

upd_rent_dto = RentUpdateRequest(
    **upd_rent
)

car = {
    "_id": "69eff1a695b371b221892947",
    "model_id": "69eff1a695b371b221892946",
    "vin": "E8NDEODTN28DCZ24B",
    "plate_number": "G510VQ285",
    "year": 2021,
    "color": "DarkGray",
    "mileage": 62109,
    "price_per_day": 3445,
    "available": True,
    "in_use": False,
    "active": True,
    "model": {
        "_id": "69eff1a695b371b221892946",
        "brand_id": "69eff1a695b371b221892945",
        "name": "Art Pro",
        "description": "High quality vehicle with redefine best-of-breed systems",
        "category": "business",
        "active": True,
        "brand": {
            "_id": "69eff1a695b371b221892945",
            "name": "Baker-Cline",
            "country": "Nicaragua",
            "description": "Young reach crime draw own student go many.",
            "active": True
        }
    }
}
car_model = CarRead(
    **car
)

user = {
    "_id": "69fae74679ac4be5cc062826",
    "email": "user_test@example.com",
    "login": "User_test",
    "first_name": "Wasya",
    "last_name": "Pupkin",
    "active": True,
    "is_admin": False,
    "is_manager": False,
    "password": "$2b$12$7EjDcL4p7YVx3EF4g20G6edK094pT1e3Q63/W66YSm5fWyNQXd0me"
}

user_ent = User(**user)

rents = [
    {
        "_id": "69eff1a595b371b221892943",
        "car_id": "69eff1a695b371b221892947",
        "client_id": "69eff19c95b371b221892930",
        "driver": False,
        "created_at": "2026-04-27T23:30:41.689000",
        "updated_at": "2026-04-27T23:30:41.689000",
        "updated_by": "69eff1a595b371b22189293a",
        "stage": "refused",
        "comment": "pappappa",
        "end_date": "2026-01-29T23:30:41.707000",
        "user_dock": "MFSLR2OA",
        "start_date": "2026-01-24T23:30:41.707000",
        "days_qty": 26,
        "total_price": 150254,
        "active": True,
        "car": {
            "_id": "69eff1a695b371b221892947",
            "model_id": "69eff19e95b371b221892932",
            "vin": "F5V7VS65FYF37FKPB",
            "plate_number": "W426NM808",
            "year": 2021,
            "color": "PowderBlue",
            "mileage": 38343,
            "price_per_day": 5779,
            "available": True,
            "in_use": False,
            "active": True,
            "model": {
                "_id": "69eff19e95b371b221892932",
                "brand_id": "69eff19d95b371b221892931",
                "name": "Dark Pro",
                "description": "High quality vehicle with cultivate visionary infrastructures",
                "category": "business",
                "active": True,
                "brand": {
                    "_id": "69eff19d95b371b221892931",
                    "name": "Robertson LLC",
                    "country": "Uzbekistan",
                    "description": "Trip forward series less next hope suddenly attack front benefit behind.",
                    "active": True
                }
            }
        },
        "client": {
            "_id": "69eff19c95b371b221892930",
            "email": "montoyachristopher@example.net",
            "login": "gilbertjillian_usr",
            "password": "$2b$12$VH2j8lYNQtMS6P556823C.RN1SGb4GhZ8214BnViAWZ14THIOWW0i",
            "first_name": "Ruth",
            "last_name": "Berry",
            "active": True,
            "is_admin": True,
            "is_manager": False
        }
    },
    {
        "_id": "69eff1a595b371b22189293e",
        "car_id": "69eff1a695b371b221892947",
        "client_id": "69eff1a595b371b22189293a",
        "driver": False,
        "created_at": "2026-04-27T23:30:45.454000",
        "updated_at": "2026-04-27T23:30:45.454000",
        "updated_by": None,
        "stage": "ordered",
        "comment": None,
        "end_date": "2026-01-05T23:30:45.294000",
        "user_dock": "QAJ1NHJ1",
        "start_date": "2026-01-04T23:30:45.294000",
        "days_qty": 6,
        "total_price": 28764,
        "active": True,
        "car": {
            "_id": "69eff1a695b371b221892947",
            "model_id": "69eff1a595b371b22189293c",
            "vin": "ZHHZ60QORPKX8KU53",
            "plate_number": "S515WL480",
            "year": 2017,
            "color": "Chartreuse",
            "mileage": 40273,
            "price_per_day": 4794,
            "available": False,
            "in_use": False,
            "active": True,
            "model": {
                "_id": "69eff1a595b371b22189293c",
                "brand_id": "69eff1a595b371b22189293b",
                "name": "Later GT",
                "description": "High quality vehicle with visualize plug-and-play web services",
                "category": "standard",
                "active": True,
                "brand": {
                    "_id": "69eff1a595b371b22189293b",
                    "name": "Lynch-Martin",
                    "country": "Malawi",
                    "description": "Hundred character hotel join lay attention see order dog begin these.",
                    "active": True
                }
            }
        },
        "client": {
            "_id": "69eff1a595b371b22189293a",
            "email": "melaniepalmer@example.org",
            "login": "mindydaniel_usr",
            "password": "$2b$12$KF/FmzOGP4u7m3bNtqVpxe/g1TLQF.j9tseD2PbURB7jC5eBVc1Jy",
            "first_name": "Brandi",
            "last_name": "Wilson",
            "active": True,
            "is_admin": False,
            "is_manager": True
        }
    },

    # {
    #   "_id": "69eff1a695b371b221892948",
    #   "car_id": "69eff1a695b371b221892947",
    #   "client_id": "69eff1a695b371b221892944",
    #   "driver": False,
    #   "created_at": "2026-04-27T23:30:46.217000",
    #   "updated_at": "2026-04-28T09:45:17.249000",
    #   "updated_by": None,
    #   "stage": "booked",
    #   "comment": None,
    #   "end_date": "2026-05-03T23:30:46.340000",
    #   "user_dock": "AAAAAAggg",
    #   "start_date": "2026-04-28T23:30:46.340000",
    #   "days_qty": 5,
    #   "total_price": 17225,
    #   "active": True,
    #   "car": {
    #     "_id": "69eff1a695b371b221892947",
    #     "model_id": "69eff1a695b371b221892946",
    #     "vin": "E8NDEODTN28DCZ24B",
    #     "plate_number": "G510VQ285",
    #     "year": 2021,
    #     "color": "DarkGray",
    #     "mileage": 62109,
    #     "price_per_day": 3445,
    #     "available": False,
    #     "in_use": False,
    #     "active": True,
    #     "model": {
    #       "_id": "69eff1a695b371b221892946",
    #       "brand_id": "69eff1a695b371b221892945",
    #       "name": "Art Pro",
    #       "description": "High quality vehicle with redefine best-of-breed systems",
    #       "category": "business",
    #       "active": True,
    #       "brand": {
    #         "_id": "69eff1a695b371b221892945",
    #         "name": "Baker-Cline",
    #         "country": "Nicaragua",
    #         "description": "Young reach crime draw own student go many.",
    #         "active": True
    #       }
    #     }
    #   },
    #   "client": {
    #     "_id": "69eff1a695b371b221892944",
    #     "email": "aliciahill@example.com",
    #     "login": "stevencampbell_usr",
    #     "password": "$2b$12$zB7DrjAjSRE7Ltsa6jKPke/qhQb3tcuSZcGjHjqJtdWcD4JwD/pYq",
    #     "first_name": "Micheal",
    #     "last_name": "Morrison",
    #     "active": True,
    #     "is_admin": False,
    #     "is_manager": False
    #   }
    # },
    # {
    #   "_id": "69f0748fd163aa7c1e018e6b",
    #   "car_id": "69eff1a595b371b221892942",
    #   "client_id": "69eff19c95b371b221892930",
    #   "driver": False,
    #   "created_at": "2026-04-28T08:49:19.418000",
    #   "updated_at": "2026-04-28T08:49:19.418000",
    #   "updated_by": None,
    #   "stage": "ordered",
    #   "comment": None,
    #   "end_date": "2026-06-29T08:35:58.445000",
    #   "user_dock": "string",
    #   "start_date": "2026-06-28T08:35:58.445000",
    #   "days_qty": 1,
    #   "total_price": 7302,
    #   "active": True,
    #   "car": {
    #     "_id": "69eff1a595b371b221892942",
    #     "model_id": "69eff1a595b371b221892941",
    #     "vin": "UP4I9FL8GK6N6LOAF",
    #     "plate_number": "C856BW537",
    #     "year": 2019,
    #     "color": "BurlyWood",
    #     "mileage": 16763,
    #     "price_per_day": 7302,
    #     "available": False,
    #     "in_use": False,
    #     "active": True,
    #     "model": {
    #       "_id": "69eff1a595b371b221892941",
    #       "brand_id": "69eff1a595b371b221892940",
    #       "name": "Trip GT",
    #       "description": "High quality vehicle with transform virtual networks",
    #       "category": "business",
    #       "active": True,
    #       "brand": {
    #         "_id": "69eff1a595b371b221892940",
    #         "name": "Simpson, Edwards and Hendricks",
    #         "country": "Maldives",
    #         "description": "Remain reflect themselves each middle certain recently last hold chair bit special why.",
    #         "active": True
    #       }
    #     }
    #   },
    #   "client": {
    #     "_id": "69eff19c95b371b221892930",
    #     "email": "montoyachristopher@example.net",
    #     "login": "gilbertjillian_usr",
    #     "password": "$2b$12$VH2j8lYNQtMS6P556823C.RN1SGb4GhZ8214BnViAWZ14THIOWW0i",
    #     "first_name": "Ruth",
    #     "last_name": "Berry",
    #     "active": True,
    #     "is_admin": True,
    #     "is_manager": False
    #   }
    # },
    # {
    #   "_id": "69f0806045604e5f404718c9",
    #   "car_id": "69eff1a695b371b221892947",
    #   "client_id": "69eff1a695b371b221892944",
    #   "driver": False,
    #   "created_at": "2026-04-28T09:39:44.373000",
    #   "updated_at": "2026-04-28T09:39:44.373000",
    #   "updated_by": "69eff1a595b371b22189293a",
    #   "stage": "paid",
    #   "comment": "dsdsfdsdf",
    #   "end_date": "2026-07-29T09:37:28.343000",
    #   "user_dock": "string",
    #   "start_date": "2026-07-28T09:37:28.343000",
    #   "days_qty": 1,
    #   "total_price": 3445,
    #   "active": True,
    #   "car": {
    #     "_id": "69eff1a695b371b221892947",
    #     "model_id": "69eff1a695b371b221892946",
    #     "vin": "E8NDEODTN28DCZ24B",
    #     "plate_number": "G510VQ285",
    #     "year": 2021,
    #     "color": "DarkGray",
    #     "mileage": 62109,
    #     "price_per_day": 3445,
    #     "available": False,
    #     "in_use": False,
    #     "active": True,
    #     "model": {
    #       "_id": "69eff1a695b371b221892946",
    #       "brand_id": "69eff1a695b371b221892945",
    #       "name": "Art Pro",
    #       "description": "High quality vehicle with redefine best-of-breed systems",
    #       "category": "business",
    #       "active": True,
    #       "brand": {
    #         "_id": "69eff1a695b371b221892945",
    #         "name": "Baker-Cline",
    #         "country": "Nicaragua",
    #         "description": "Young reach crime draw own student go many.",
    #         "active": True
    #       }
    #     }
    #   },
    #   "client": {
    #     "_id": "69eff1a695b371b221892944",
    #     "email": "aliciahill@example.com",
    #     "login": "stevencampbell_usr",
    #     "password": "$2b$12$zB7DrjAjSRE7Ltsa6jKPke/qhQb3tcuSZcGjHjqJtdWcD4JwD/pYq",
    #     "first_name": "Micheal",
    #     "last_name": "Morrison",
    #     "active": True,
    #     "is_admin": False,
    #     "is_manager": False
    #   }
    # },
    # {
    #   "_id": "69f09e72f949c172a20c66d3",
    #   "car_id": "69eff1a595b371b22189293d",
    #   "client_id": "69f09df1f949c172a20c66d2",
    #   "driver": False,
    #   "created_at": "2026-04-28T11:48:02.735000",
    #   "updated_at": "2026-04-28T11:52:02.567000",
    #   "updated_by": None,
    #   "stage": "ordered",
    #   "comment": None,
    #   "end_date": "2026-05-28T11:49:05.995000",
    #   "user_dock": "string",
    #   "start_date": "2026-04-28T11:49:05.995000",
    #   "days_qty": 30,
    #   "total_price": 143820,
    #   "active": True,
    #   "car": {
    #     "_id": "69eff1a595b371b22189293d",
    #     "model_id": "69eff1a595b371b22189293c",
    #     "vin": "ZHHZ60QORPKX8KU53",
    #     "plate_number": "S515WL480",
    #     "year": 2017,
    #     "color": "Chartreuse",
    #     "mileage": 40273,
    #     "price_per_day": 4794,
    #     "available": False,
    #     "in_use": False,
    #     "active": True,
    #     "model": {
    #       "_id": "69eff1a595b371b22189293c",
    #       "brand_id": "69eff1a595b371b22189293b",
    #       "name": "Later GT",
    #       "description": "High quality vehicle with visualize plug-and-play web services",
    #       "category": "standard",
    #       "active": True,
    #       "brand": {
    #         "_id": "69eff1a595b371b22189293b",
    #         "name": "Lynch-Martin",
    #         "country": "Malawi",
    #         "description": "Hundred character hotel join lay attention see order dog begin these.",
    #         "active": True
    #       }
    #     }
    #   },
    #   "client": {
    #     "_id": "69f09df1f949c172a20c66d2",
    #     "email": "dossapeuxiju-9642@yopmail.com",
    #     "login": "AAAaaa",
    #     "password": "$2b$12$uuyd8n6PBXMdnJXVRcuzl.UxLj/5O4kuvo8JgE/R4RjZgPHypZgQe",
    #     "first_name": "Wasya",
    #     "last_name": "Puokin",
    #     "active": True,
    #     "is_admin": False,
    #     "is_manager": False
    #   }
    # }
]

rents_list = [RentRead(**r) for r in rents]

rent = {
    "_id": "69eff1a595b371b221892943",
    "car_id": "69eff1a595b371b221892942",
    "client_id": "69fae74679ac4be5cc062826",
    "driver": False,
    "created_at": "2026-04-27T23:30:45.746000",
    "updated_at": "2026-04-27T23:30:45.746000",
    "updated_by": None,
    "stage": "ordered",
    "comment": None,
    "end_date": "2026-06-21T23:30:45.593000",
    "user_dock": "MOYQ8MBO",
    "start_date": "2026-04-28T23:30:45.593000",
    "days_qty": 54,
    "total_price": 394308,
    "active": True,
    "car": {
        "_id": "69eff1a595b371b221892942",
        "model_id": "69eff1a595b371b221892941",
        "vin": "UP4I9FL8GK6N6LOAF",
        "plate_number": "C856BW537",
        "year": 2019,
        "color": "BurlyWood",
        "mileage": 16763,
        "price_per_day": 7302,
        "available": False,
        "in_use": False,
        "active": True,
        "model": {
            "_id": "69eff1a595b371b221892941",
            "brand_id": "69eff1a595b371b221892940",
            "name": "Trip GT",
            "description": "High quality vehicle with transform virtual networks",
            "category": "business",
            "active": True,
            "brand": {
                "_id": "69eff1a595b371b221892940",
                "name": "Simpson, Edwards and Hendricks",
                "country": "Maldives",
                "description": "Remain reflect themselves each middle certain recently last hold chair bit special why.",
                "active": True
            }
        }
    },
    "client": {
        "_id": "69fae74679ac4be5cc062826",
        "email": "quinnjose@example.net",
        "login": "kirbytammy_usr",
        "password": "$2b$12$6XI5CnlftC5Om15MV4MzGe.aVU6ExnMKWqq52AzXOXv/FqwCae1Py",
        "first_name": "Emily",
        "last_name": "Williams",
        "active": True,
        "is_admin": False,
        "is_manager": False
    }
}

rent_ent = RentRead(
    **rent
)


@pytest.fixture
def mock_user_repo():
    mock = AsyncMock()
    mock.create.side_effect = lambda x: x
    # mock.get_by_id.side_effect = lambda x: x
    mock.find_for_logining.return_value = user_ent
    return mock


@pytest.fixture
def mock_car_repo():
    mock = AsyncMock()
    return mock


@pytest.fixture
def mock_rent_repo():
    mock = AsyncMock()
    return mock


@pytest.fixture
def rent_service(mock_rent_repo, mock_user_repo, mock_car_repo):
    return RentService(mock_rent_repo, mock_user_repo, mock_car_repo)
