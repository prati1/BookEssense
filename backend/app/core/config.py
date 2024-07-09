from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    google_client_id: str
    google_client_secret: str

    class Config:
        env_file = ".env"

settings = Settings()
