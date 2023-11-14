from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_secret: str = "replace-me"
    app_url: str = "http://localhost:8000"
    database_url: str = "sqlite:///:memory:"
    google_client_id: str = ""

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
