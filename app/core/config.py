from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "Cars REST API"
    app_version: str = "1.0.0"
    app_description: str = "A REST service to manage cars with full CRUD operations"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    class Config:
        env_file = ".env"


settings = Settings()
