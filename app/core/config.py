from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    MONGO_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "homeopathy_hospital"
    SECRET_KEY: str = "y0ur_sup3r_s3cr3t_k3y_h3r3_m4k3_1t_l0ng_4nd_r4nd0m"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    STATIC_DIR: str = "app/static/medicines"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

# Ensure static directory exists
os.makedirs(settings.STATIC_DIR, exist_ok=True)
