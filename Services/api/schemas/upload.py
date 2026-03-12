from pydantic import BaseModel, Field
from datetime import datetime


class UploadResponse(BaseModel):
    job_id: str = Field(..., description="Unique job identifier")
    video_id: str = Field(..., description="Unique video identifier")
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="File size in bytes")
    status: str = Field(default="PENDING", description="Initial job status")
    created_at: datetime = Field(..., description="Upload timestamp")

    class Config:
        from_attributes = True
