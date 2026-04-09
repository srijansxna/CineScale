from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class VideoMetadata(BaseModel):
    duration: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
    codec: Optional[str] = None
    bitrate: Optional[int] = None
    fps: Optional[float] = None


class VideoVariant(BaseModel):
    resolution: str
    width: int
    height: int
    file_size: Optional[int] = None
    url: Optional[str] = None
    status: str


class ProcessingStatus(BaseModel):
    status: str
    progress: int = Field(..., ge=0, le=100)
    job_id: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None


class VideoDetailResponse(BaseModel):
    video_id: str
    filename: str
    file_size: int
    content_type: Optional[str] = None
    is_pinned: bool = False
    video_title: Optional[str] = None
    default_thumbnail: Optional[str] = None
    final_thumbnail_url: Optional[str] = None
    metadata: Optional[VideoMetadata] = None
    variants: List[VideoVariant] = []
    thumbnails: List[str] = []
    processing: ProcessingStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True
