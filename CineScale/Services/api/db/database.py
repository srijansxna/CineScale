import redis
from services.api.config import get_settings

settings = get_settings()


def get_redis_client(db: int = 0) -> redis.Redis:
    """Get Redis client for specified database."""
    return redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=db,
        decode_responses=True
    )


def get_status_db() -> redis.Redis:
    """Get Redis client for job status storage."""
    return get_redis_client(db=settings.redis_status_db)
