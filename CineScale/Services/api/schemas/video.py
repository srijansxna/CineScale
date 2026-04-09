from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime


class VideoMetadata(BaseModel):
    duration: float
    width: int
    height: int
    codec: str


class VideoUploadResponse(BaseModel):
    job_id: str
    status: str
    filename: str


class VideoInfo(BaseModel):
    job_id: str
    filename: str
    status: str
    metadata: Optional[VideoMetadata] = None
    thumbnails: Optional[List[str]] = None
    created_at: Optional[str] = None
