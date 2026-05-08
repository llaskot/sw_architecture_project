from unittest.mock import AsyncMock
import os
import pytest

os.environ.update({
    "MAILER_HOST": "mock",
    "MAILER_PORT": "465",
    "MAILER_USER": "test@test.com",
    "MAILER_PASS": "pass",
    "MONGO_USER": "root",
    "MONGO_PASSWORD": "pass",
    "MONGO_PORT": "27017",
    "SECRET_KEY": "secret",
    "JWT_SOLT": "hgffvghMBk4kjllnLHLlhlh656464sdJJJJJJldtfjgDffFKF12345",
    "AUTH_SECRET_KEY": "very_secret_key" # Специально для твоего AuthService
})

from app.auth.service import AuthService
from app.users.service import UserService
from app.users.user_model import User

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


@pytest.fixture
def mock_user_repo():
    mock = AsyncMock()
    mock.create.side_effect = lambda x: x
    mock.get_by_id.side_effect = lambda x: x
    mock.find_for_logining.return_value = user_ent
    return mock


@pytest.fixture
def auth_service(mock_user_repo):
    return AuthService(mock_user_repo)
