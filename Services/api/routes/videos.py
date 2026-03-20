import os
from pathlib import Path
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse

from services.api.schemas.video_detail import (
    VideoDetailResponse, VideoMetadata, VideoVariant, ProcessingStatus,
)
from services.api.services.video_service import VideoService, get_video_service
from services.api.db.pg_models import JobStatus

router = APIRouter()


def _build_response(video, job) -> VideoDetailResponse:
    """Build a VideoDetailResponse from ORM objects."""
    metadata = None
    variants: list = []
    thumbnails: list = []

    if job.result and job.status == JobStatus.DONE:
        if "metadata" in job.result:
            m = job.result["metadata"]
            metadata = VideoMetadata(
                duration=m.get("duration"),
                width=m.get("width"),
                height=m.get("height"),
                codec=m.get("codec"),
                bitrate=m.get("bitrate"),
                fps=m.get("fps"),
            )

        if "variants" in job.result:
            for v in job.result["variants"]:
                variants.append(VideoVariant(
                    resolution=v["resolution"],
                    width=v["width"],
                    height=v["height"],
                    file_size=v.get("file_size"),
                    url=f"/api/videos/{video.video_id}/stream/{v['resolution']}",
                    status=v.get("status", "ready"),
                ))

        if "thumbnails" in job.result:
            thumbnails = [
                f"/api/videos/{video.video_id}/thumbnails/{Path(t).name}"
                for t in job.result["thumbnails"]
            ]

    processing = ProcessingStatus(
        status=job.status.value,
        progress=job.progress,
        job_id=job.job_id,
        started_at=job.updated_at if job.status != JobStatus.PENDING else None,
        completed_at=job.updated_at if job.status in (
            JobStatus.DONE, JobStatus.FAILED) else None,
        error=job.error,
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
        updated_at=video.updated_at,
    )


@router.get("/videos", response_model=List[VideoDetailResponse])
async def list_videos(video_service: VideoService = Depends(get_video_service)):
    """List all uploaded videos with their processing status."""
    pairs = await video_service.get_all_videos()
    return [_build_response(video, job) for video, job in pairs]


@router.get("/videos/{video_id}", response_model=VideoDetailResponse)
async def get_video_detail(
    video_id: str,
    video_service: VideoService = Depends(get_video_service),
):
    """Get complete video information."""
    video = await video_service.get_video_by_id(video_id)
    if not video:
        raise HTTPException(404, f"Video {video_id} not found")

    job = await video_service.get_job_by_video_id(video_id)
    if not job:
        raise HTTPException(
            404, f"No processing job found for video {video_id}")

    return _build_response(video, job)


@router.get("/videos/{video_id}/stream/{resolution}")
async def stream_video(
    video_id: str,
    resolution: str,
    video_service: VideoService = Depends(get_video_service),
):
    """Stream video at specified resolution."""
    video = await video_service.get_video_by_id(video_id)
    if not video:
        raise HTTPException(404, "Video not found")

    video_path = f"storage/output/{video_id}/{resolution}.mp4"
    if not os.path.exists(video_path):
        # Try the actual filename pattern: {stem}_{resolution}.mp4
        stem = Path(video.file_path).stem
        video_path = f"storage/output/{video_id}/{stem}_{resolution}.mp4"
    if not os.path.exists(video_path):
        video_path = video.file_path
        if not os.path.exists(video_path):
            raise HTTPException(404, "Video file not found")

    return FileResponse(
        video_path,
        media_type="video/mp4",
        filename=f"{Path(video.filename).stem}_{resolution}.mp4",
    )


@router.get("/videos/{video_id}/thumbnails/{thumbnail_name}")
async def get_thumbnail(
    video_id: str,
    thumbnail_name: str,
    video_service: VideoService = Depends(get_video_service),
):
    """Get a video thumbnail."""
    video = await video_service.get_video_by_id(video_id)
    if not video:
        raise HTTPException(404, "Video not found")

    # Thumbnails are saved inside the output dir alongside transcoded files
    thumbnail_path = f"storage/output/{video_id}/{thumbnail_name}"
    if not os.path.exists(thumbnail_path):
        raise HTTPException(404, "Thumbnail not found")

    return FileResponse(thumbnail_path, media_type="image/jpeg", filename=thumbnail_name)
