from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.schemas.upload import UploadResponse
from services.api.services.video_service import VideoService, get_video_service
from services.api.config import get_settings
from services.api.celery_client import celery_app

router = APIRouter()
settings = get_settings()


@router.post("/upload", response_model=UploadResponse)
async def upload_video(
    file: UploadFile = File(..., description="Video file to upload"),
    video_service: VideoService = Depends(get_video_service),
):
    """
    Upload a video file for processing.

    Flow:
    1. Validate file type / size
    2. Save file to local storage
    3. Create Video + ProcessingJob records in PostgreSQL
    4. Dispatch process_video task to Celery / Redis queue
    5. Return job_id and video_id
    """
    # Validate extension
    allowed_extensions = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv", ".wmv"}
    file_extension = f".{file.filename.lower().rsplit('.', 1)[-1]}" if file.filename else ""

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}",
        )

    # Validate size (when Content-Length is provided)
    if file.size and file.size > settings.max_upload_size:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max size: {settings.max_upload_size} bytes",
        )

    # 1. Save file + persist DB records
    video, job = await video_service.create_video_and_job(file)

    # 2. Build the job payload the worker expects
    output_dir = f"{settings.storage_output_dir}/{video.video_id}"
    task_payload = {
        "job_id": job.job_id,
        "input_path": video.file_path,
        "output_dir": output_dir,
    }

    # 3. Push to Redis queue via Celery
    celery_app.send_task(
        "services.worker.tasks.process_video",
        args=[task_payload],
        task_id=job.job_id,  # use job_id as Celery task id for easy lookup
    )

    return UploadResponse(
        job_id=job.job_id,
        video_id=video.video_id,
        filename=video.filename,
        file_size=video.file_size,
        status=job.status.value,
        created_at=video.created_at,
    )
