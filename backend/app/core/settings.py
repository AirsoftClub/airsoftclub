from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """This class preloads configs from .env file."""

    app_secret: str
    app_url: str = "http://localhost:8000"
    google_client_id: str

    # Define your DB settings here as well
    db_user: str
    db_pass: str
    db_host: str
    db_port: str
    db_name: str

    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg2://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
