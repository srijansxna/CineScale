from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.schemas.job_status import JobStatusResponse
from services.api.services.video_service import VideoService, get_video_service
from services.api.db.postgres import get_db

router = APIRouter()


@router.get("/job/{job_id}", response_model=JobStatusResponse)
async def get_job_status(
    job_id: str,
    video_service: VideoService = Depends(get_video_service)
):
    """
    Get the status of a video processing job.
    
    **Job States:**
    - `PENDING` - Job created, waiting to be processed (progress: 0%)
    - `PROCESSING` - Job is currently being processed (progress: 1-99%)
    - `DONE` - Job completed successfully (progress: 100%)
    - `FAILED` - Job failed with error (progress: varies)
    
    **Returns:**
    - job_id: Unique job identifier
    - video_id: Associated video identifier
    - status: Current job state
    - progress: Progress percentage (0-100)
    - result: Processing results (when DONE)
    - error: Error message (when FAILED)
    - created_at: Job creation timestamp
    - updated_at: Last update timestamp
    """
    job = await video_service.get_job_by_id(job_id)
    
    if not job:
        raise HTTPException(
            status_code=404,
            detail=f"Job {job_id} not found"
        )
    
    return JobStatusResponse(
        job_id=job.job_id,
        video_id=job.video_id,
        status=job.status.value,
        progress=job.progress,
        result=job.result,
        error=job.error,
        created_at=job.created_at,
        updated_at=job.updated_at
    )


@router.delete("/job/{job_id}")
async def delete_job(
    job_id: str,
    video_service: VideoService = Depends(get_video_service)
):
    """
    Delete a job and its associated data.
    
    **Note:** This does not delete the video file or video record.
    """
    job = await video_service.get_job_by_id(job_id)
    
    if not job:
        raise HTTPException(
            status_code=404,
            detail=f"Job {job_id} not found"
        )
    
    deleted = await video_service.delete_job(job_id)
    
    return {
        "job_id": job_id,
        "deleted": deleted,
        "message": "Job deleted successfully"
    }
