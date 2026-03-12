from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.schemas.upload import UploadResponse
from services.api.services.video_service import VideoService, get_video_service
from services.api.db.postgres import get_db
from services.api.config import get_settings

router = APIRouter()
settings = get_settings()


@router.post("/upload", response_model=UploadResponse)
async def upload_video(
    file: UploadFile = File(..., description="Video file to upload"),
    video_service: VideoService = Depends(get_video_service)
):
    """
    Upload a video file for processing.
    
    **Requirements:**
    - Accept video file upload
    - Save file locally
    - Generate video_id
    - Create a processing job entry in PostgreSQL
    - Return job_id and video_id
    
    **Process:**
    1. Validates file type (must be video)
    2. Generates unique video_id and job_id
    3. Saves file to local storage
    4. Creates Video record in PostgreSQL
    5. Creates ProcessingJob record in PostgreSQL
    6. Returns job and video information
    """
    # Validate file extension
    allowed_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv'}
    file_extension = file.filename.lower().split('.')[-1] if file.filename else ''
    
    if not file_extension or f'.{file_extension}' not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Validate file size
    if file.size and file.size > settings.max_upload_size:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max size: {settings.max_upload_size} bytes"
        )
    
    # Create video and job records
    video, job = await video_service.create_video_and_job(file)
    
    return UploadResponse(
        job_id=job.job_id,
        video_id=video.video_id,
        filename=video.filename,
        file_size=video.file_size,
        status=job.status.value,
        created_at=video.created_at
    )
