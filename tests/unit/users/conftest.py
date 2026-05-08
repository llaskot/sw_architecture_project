from unittest.mock import AsyncMock

import pytest

from app.users.service import UserService


@pytest.fixture
def mock_user_repo():
    mock = AsyncMock()
    mock.create.side_effect = lambda x: x
    return mock

@pytest.fixture
def user_service(mock_user_repo):
    return UserService(repo=mock_user_repo)