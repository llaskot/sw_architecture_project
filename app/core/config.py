from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Данные для почты
    mailer_host: str
    mailer_port: int
    mailer_user: str
    mailer_pass: str


    # database_url: str
    mongo_user: str
    mongo_password: str
    mongo_port: int

    secret_key: str
    jwt_solt: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")



settings = Settings()