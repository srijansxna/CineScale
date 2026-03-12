from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Application
    app_name: str = "CineScale"
    debug: bool = False
    
    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/cinescale"
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_broker_db: int = 0
    redis_backend_db: int = 1
    redis_status_db: int = 2
    
    # Storage
    storage_raw_dir: str = "storage/raw"
    storage_output_dir: str = "storage/output"
    storage_thumbnails_dir: str = "storage/thumbnails"
    max_upload_size: int = 500 * 1024 * 1024  # 500MB
    
    # Celery
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
