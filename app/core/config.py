from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field

class Settings(BaseSettings):
    mailer_host: str
    mailer_port: int
    mailer_user: str
    mailer_pass: str

    mongo_user: str
    mongo_password: str
    mongo_port: int
    # дефолт "localhost" для локальной разработки
    mongo_host: str = "localhost"
    mongo_db: str = "test_db"

    secret_key: str
    jwt_solt: str
    upload_dir: str

    expose_host: str
    expose_app_port: str

    vite_api_url: str

    first_admin_login: str | None = None
    first_admin_pass: str | None = None
    first_admin_mail: str | None = None
    first_admin_name: str | None = None

    # само соберет строку подключения
    @computed_field
    @property
    def database_url(self) -> str:
        return f"mongodb://{self.mongo_user}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}/{self.mongo_db}?authSource=admin"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore" # игнорировать лишние переменные в .env
    )

settings = Settings()