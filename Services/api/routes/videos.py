from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from typing import Optional

from services.api.schemas.video_detail import VideoDetailResponse, VideoMetadata, VideoVariant, ProcessingStatus
from services.api.services.video_service import VideoService, get_video_service
from services.api.db.models import JobStatus

router = APIRouter()


@router.get("/videos/{video_id}", response_model=VideoDetailResponse)
async def get_video_detail(
    video_id: str,
    video_service: VideoService = Depends(get_video_service)
):
    """
    Get complete video information including metadata, variants, thumbnails, and processing status.
    
    **Returns:**
    - Video metadata (duration, resolution, codec, etc.)
    - Available variants/resolutions (720p, 1080p, etc.)
    - Thumbnail URLs
    - Processing status and progress
    
    **Use Cases:**
    - Display video information in UI
    - Check processing status
    - Get streaming URLs for different resolutions
    - Show thumbnails for video preview
    """
    # Get video record
    video = await video_service.get_video_by_id(video_id)
    if not video:
        raise HTTPException(
            status_code=404,
            detail=f"Video {video_id} not found"
        )
    
    # Get associated job
    job = await video_service.get_job_by_video_id(video_id)
    if not job:
        raise HTTPException(
            status_code=404,
            detail=f"No processing job found for video {video_id}"
        )
    
    # Build metadata from job result
    metadata = None
    variants = []
    thumbnails = []
    
    if job.result and job.status == JobStatus.DONE:
        # Extract metadata
        if "metadata" in job.result:
            meta = job.result["metadata"]
            metadata = VideoMetadata(
                duration=meta.get("duration"),
                width=meta.get("width"),
                height=meta.get("height"),
                codec=meta.get("codec"),
                bitrate=meta.get("bitrate"),
                fps=meta.get("fps")
            )
        
        # Extract variants
        if "variants" in job.result:
            for variant in job.result["variants"]:
                variants.append(VideoVariant(
                    resolution=variant["resolution"],
                    width=variant["width"],
                    height=variant["height"],
                    file_size=variant.get("file_size"),
                    url=f"/api/videos/{video_id}/stream/{variant['resolution']}",
                    status=variant.get("status", "ready")
                ))
        
        # Extract thumbnails
        if "thumbnails" in job.result:
            thumbnails = [
                f"/api/videos/{video_id}/thumbnails/{thumb}"
                for thumb in job.result["thumbnails"]
            ]
    
    # Build processing status
    processing = ProcessingStatus(
        status=job.status.value,
        progress=job.progress,
        job_id=job.job_id,
        started_at=job.updated_at if job.status != JobStatus.PENDING else None,
        completed_at=job.updated_at if job.status in [JobStatus.DONE, JobStatus.FAILED] else None,
        error=job.error
    )
    
    return VideoDetailResponse(
        video_id=video.video_id,
        filename=video.filename,
        file_size=video.file_size,
        content_type=video.content_type,
        metadata=metadata,
        variants=variants,
        thumbnails=thumbnails,
        processing=processing,
        created_at=video.created_at,
        updated_at=video.updated_at
    )


@router.get("/videos/{video_id}/stream/{resolution}")
async def stream_video(
    video_id: str,
    resolution: str,
    video_service: VideoService = Depends(get_video_service)
):
    """
    Stream video at specified resolution.
    
    **Resolutions:** 240p, 360p, 480p, 720p, 1080p, 1440p, 4k
    """
    video = await video_service.get_video_by_id(video_id)
    if not video:
        raise HTTPException(404, f"Video {video_id} not found")
    
    # Construct video path for variant
    video_path = f"storage/output/{video_id}/{resolution}.mp4"
    
    # Check if variant exists
    import os
    if not os.path.exists(video_path):
        # Fall back to original if variant doesn't exist
        video_path = video.file_path
        if not os.path.exists(video_path):
            raise HTTPException(404, f"Video file not found")
    
    return FileResponse(
        video_path,
        media_type="video/mp4",
        filename=f"{video.filename.rsplit('.', 1)[0]}_{resolution}.mp4"
    )


@router.get("/videos/{video_id}/thumbnails/{thumbnail_name}")
async def get_thumbnail(
    video_id: str,
    thumbnail_name: str,
    video_service: VideoService = Depends(get_video_service)
):
    """
    Get video thumbnail image.
    """
    video = await video_service.get_video_by_id(video_id)
    if not video:
        raise HTTPException(404, f"Video {video_id} not found")
    
    # Construct thumbnail path
    thumbnail_path = f"storage/thumbnails/{video_id}/{thumbnail_name}"
    
    import os
    if not os.path.exists(thumbnail_path):
        raise HTTPException(404, f"Thumbnail not found")
    
    return FileResponse(
        thumbnail_path,
        media_type="image/jpeg",
        filename=thumbnail_name
    )
