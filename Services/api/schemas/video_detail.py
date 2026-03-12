from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime


class VideoMetadata(BaseModel):
    """Video metadata information."""
    duration: Optional[float] = Field(None, description="Video duration in seconds")
    width: Optional[int] = Field(None, description="Video width in pixels")
    height: Optional[int] = Field(None, description="Video height in pixels")
    codec: Optional[str] = Field(None, description="Video codec")
    bitrate: Optional[int] = Field(None, description="Bitrate in kbps")
    fps: Optional[float] = Field(None, description="Frames per second")


class VideoVariant(BaseModel):
    """Video variant/resolution information."""
    resolution: str = Field(..., description="Resolution (e.g., 720p, 1080p)")
    width: int = Field(..., description="Width in pixels")
    height: int = Field(..., description="Height in pixels")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    url: Optional[str] = Field(None, description="Streaming URL")
    status: str = Field(..., description="Variant status: pending, processing, ready, failed")


class ProcessingStatus(BaseModel):
    """Processing status information."""
    status: str = Field(..., description="Overall status: PENDING, PROCESSING, DONE, FAILED")
    progress: int = Field(..., ge=0, le=100, description="Progress percentage")
    job_id: str = Field(..., description="Associated job ID")
    started_at: Optional[datetime] = Field(None, description="Processing start time")
    completed_at: Optional[datetime] = Field(None, description="Processing completion time")
    error: Optional[str] = Field(None, description="Error message if failed")


class VideoDetailResponse(BaseModel):
    """Complete video information response."""
    video_id: str = Field(..., description="Unique video identifier")
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="Original file size in bytes")
    content_type: Optional[str] = Field(None, description="MIME type")
    
    metadata: Optional[VideoMetadata] = Field(None, description="Video metadata")
    variants: List[VideoVariant] = Field(default_factory=list, description="Available video variants/resolutions")
    thumbnails: List[str] = Field(default_factory=list, description="Thumbnail URLs")
    
    processing: ProcessingStatus = Field(..., description="Processing status")
    
    created_at: datetime = Field(..., description="Upload timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "video_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                "filename": "demo.mp4",
                "file_size": 15728640,
                "content_type": "video/mp4",
                "metadata": {
                    "duration": 120.5,
                    "width": 1920,
                    "height": 1080,
                    "codec": "h264",
                    "bitrate": 5000,
                    "fps": 30.0
                },
                "variants": [
                    {
                        "resolution": "1080p",
                        "width": 1920,
                        "height": 1080,
                        "file_size": 15728640,
                        "url": "/api/videos/6ba7b810/stream/1080p",
                        "status": "ready"
                    },
                    {
                        "resolution": "720p",
                        "width": 1280,
                        "height": 720,
                        "file_size": 8388608,
                        "url": "/api/videos/6ba7b810/stream/720p",
                        "status": "ready"
                    }
                ],
                "thumbnails": [
                    "/api/videos/6ba7b810/thumbnails/thumb_1.jpg",
                    "/api/videos/6ba7b810/thumbnails/thumb_2.jpg"
                ],
                "processing": {
                    "status": "DONE",
                    "progress": 100,
                    "job_id": "550e8400-e29b-41d4-a716-446655440000",
                    "started_at": "2024-03-12T10:30:00Z",
                    "completed_at": "2024-03-12T10:32:00Z",
                    "error": None
                },
                "created_at": "2024-03-12T10:30:00Z",
                "updated_at": "2024-03-12T10:32:00Z"
            }
        }
