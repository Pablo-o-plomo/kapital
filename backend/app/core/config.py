from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "postgresql+psycopg://ops_user:ops_password@db:5432/ops_director"
    backend_cors_origins: str = "http://localhost:3000"
    app_env: str = "production"
    iiko_api_login: str = ""
    iiko_base_url: str = "https://api-ru.iiko.services"


settings = Settings()
