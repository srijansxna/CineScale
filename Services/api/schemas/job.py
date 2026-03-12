from pydantic import BaseModel
from typing import Optional, Dict, Any
from services.api.db.models import JobStatus


class JobStatusResponse(BaseModel):
    job_id: str
    status: JobStatus
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class JobCreateRequest(BaseModel):
    job_id: str
    input_path: str
    output_dir: str
