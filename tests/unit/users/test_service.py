
from app.users.schemas import UserCreate


async def test_create_user_success(user_service, mock_user_repo):
    raw_password = "super_secret_password"
    user_data = UserCreate(
        email = "test@example.com" ,
        login = 'testUser',
        password=raw_password,
        first_name='testFirstName',
        last_name='testLastName',
    )
    result: UserCreate = await user_service.create(user_data)

    # Assert: Проверяем результат
    # 1. Вызвался ли метод репозитория?
    mock_user_repo.create.assert_called_once()

    # 2. Главное: пароль в базе не должен быть сырым
    assert result.password != raw_password
    # 3. Проверяем, что это вообще похоже на хеш (bcrypt начинается с $2b$)
    assert result.password.startswith("$2b$")
    assert result.is_manager == False
    assert result.is_admin == False
    assert result.active == True
    assert result.first_name == "testFirstName"
    assert result.last_name == "testLastName"
    assert result.email == "test@example.com"