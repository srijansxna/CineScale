from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class JobStatusResponse(BaseModel):
    """Response model for job status."""
    
    job_id: str = Field(..., description="Unique job identifier")
    video_id: str = Field(..., description="Associated video identifier")
    status: str = Field(..., description="Current job status: PENDING, PROCESSING, DONE, FAILED")
    progress: int = Field(..., ge=0, le=100, description="Progress percentage (0-100)")
    result: Optional[Dict[str, Any]] = Field(None, description="Processing result data (available when DONE)")
    error: Optional[str] = Field(None, description="Error message (available when FAILED)")
    created_at: datetime = Field(..., description="Job creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "job_id": "550e8400-e29b-41d4-a716-446655440000",
                "video_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                "status": "PROCESSING",
                "progress": 45,
                "result": None,
                "error": None,
                "created_at": "2024-03-12T10:30:00Z",
                "updated_at": "2024-03-12T10:30:45Z"
            }
        }
