from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'Restaurant Ops Control API'
    app_env: str = 'development'
    database_url: str = 'postgresql+psycopg://ops_user:ops_password@db:5432/ops_director'
    jwt_secret: str = 'change_this_secret'
    jwt_algorithm: str = 'HS256'
    access_token_expire_minutes: int = 60 * 24
    backend_cors_origins: str = 'http://localhost:3000'


settings = Settings()
