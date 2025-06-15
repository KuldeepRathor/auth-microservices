from pydantic import BaseModel
from typing import List
from functools import lru_cache
import os


class Settings(BaseModel):
    # Database - using SQLite for now
    database_url: str = "sqlite:///./auth.db"
    test_database_url: str = "sqlite:///./test_auth.db"
    
    # JWT Configuration
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Application Settings
    api_v1_str: str = "/api/v1"
    project_name: str = "Auth Microservice"
    debug: bool = True
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]


@lru_cache()
def get_settings() -> Settings:
    return Settings()
