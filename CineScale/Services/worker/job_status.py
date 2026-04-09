import redis
import json
import os
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Get Redis configuration from environment
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
STATUS_DB = os.getenv("REDIS_STATUS_DB", "2")

# Initialize Redis connection
r = redis.Redis(
    host=REDIS_HOST,
    port=int(REDIS_PORT),
    db=int(STATUS_DB),
    decode_responses=True
)


def set_status(job_id: str, status: str, extra: Optional[Dict[str, Any]] = None) -> None:
    """
    Set job status in Redis.
    
    Args:
        job_id: Unique job identifier
        status: Job status (PENDING, PROCESSING, COMPLETED, FAILED)
        extra: Additional data to store with status
    """
    payload = {"status": status}
    
    if extra:
        payload.update(extra)
    
    try:
        r.set(job_id, json.dumps(payload))
        logger.debug(f"Status updated for job {job_id}: {status}")
    except Exception as e:
        logger.error(f"Failed to set status for job {job_id}: {e}")
        raise


def get_status(job_id: str) -> Optional[Dict[str, Any]]:
    """
    Get job status from Redis.
    
    Args:
        job_id: Unique job identifier
    
    Returns:
        Dictionary with job status and metadata, or None if not found
    """
    try:
        data = r.get(job_id)
        if not data:
            return None
        return json.loads(data)
    except Exception as e:
        logger.error(f"Failed to get status for job {job_id}: {e}")
        return None


def update_progress(job_id: str, progress: int, step: str) -> None:
    """
    Update job progress.
    
    Args:
        job_id: Unique job identifier
        progress: Progress percentage (0-100)
        step: Current processing step
    """
    current_status = get_status(job_id)
    
    if current_status:
        current_status["progress"] = progress
        current_status["step"] = step
        r.set(job_id, json.dumps(current_status))
        logger.debug(f"Progress updated for job {job_id}: {progress}% ({step})")
    else:
        logger.warning(f"Cannot update progress for non-existent job: {job_id}")


def delete_status(job_id: str) -> bool:
    """
    Delete job status from Redis.
    
    Args:
        job_id: Unique job identifier
    
    Returns:
        True if deleted, False if not found
    """
    try:
        result = r.delete(job_id)
        return result > 0
    except Exception as e:
        logger.error(f"Failed to delete status for job {job_id}: {e}")
        return False


def get_all_jobs() -> Dict[str, Dict[str, Any]]:
    """
    Get all job statuses from Redis.
    
    Returns:
        Dictionary mapping job_id to status data
    """
    try:
        jobs = {}
        for key in r.scan_iter():
            data = r.get(key)
            if data:
                jobs[key] = json.loads(data)
        return jobs
    except Exception as e:
        logger.error(f"Failed to get all jobs: {e}")
        return {}
