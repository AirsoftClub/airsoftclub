from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_secret: str = ""
    app_url: str = ""
    database_url: str = ""
    google_client_id: str = ""

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
