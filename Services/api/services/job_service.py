import json
from typing import Optional, Dict, Any
from services.api.db.database import get_status_db
from services.api.db.models import JobStatus
from services.api.schemas.job import JobStatusResponse


class JobService:
    """Service for managing job status and operations."""
    
    def __init__(self):
        self.redis = get_status_db()
    
    def set_status(
        self,
        job_id: str,
        status: JobStatus,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None
    ) -> None:
        """Set job status in Redis."""
        payload = {
            "status": status.value,
            "result": result,
            "error": error
        }
        self.redis.set(job_id, json.dumps(payload))
    
    def get_status(self, job_id: str) -> Optional[JobStatusResponse]:
        """Get job status from Redis."""
        data = self.redis.get(job_id)
        if not data:
            return None
        
        payload = json.loads(data)
        return JobStatusResponse(
            job_id=job_id,
            status=JobStatus(payload["status"]),
            result=payload.get("result"),
            error=payload.get("error")
        )
    
    def delete_job(self, job_id: str) -> bool:
        """Delete job from Redis."""
        return bool(self.redis.delete(job_id))
    
    def job_exists(self, job_id: str) -> bool:
        """Check if job exists."""
        return bool(self.redis.exists(job_id))


def get_job_service() -> JobService:
    """Dependency for job service."""
    return JobService()
