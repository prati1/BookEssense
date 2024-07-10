from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    google_client_id: str
    google_client_secret: str
    llm_type: str
    llm_api_key: str
    ollama_base_url: str

    class Config:
        env_file = ".env"

settings = Settings()
