from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    app_name: str = "Sentinel-AURA Backend"
    app_version: str = "1.0.0"
    debug: bool = True

    host: str = "0.0.0.0"
    port: int = 8000

    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "aura_db"

    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]

    log_level: str = "INFO"

    model_config = {"env_file": ".env"}

settings = Settings()