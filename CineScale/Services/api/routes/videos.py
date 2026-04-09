import os
from pathlib import Path
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse

from services.api.schemas.video_detail import (
    VideoDetailResponse, VideoMetadata, VideoVariant, ProcessingStatus,
)
from services.api.schemas.thumbnail_config import ThumbnailConfigRequest, ThumbnailConfigResponse
from services.api.services.video_service import VideoService, get_video_service
from services.api.db.pg_models import JobStatus
from services.transcoder.thumbnails import apply_text_overlay, THUMBNAIL_KEY_MAP

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
        is_pinned=getattr(video, 'is_pinned', False),
        video_title=getattr(video, 'video_title', None),
        default_thumbnail=getattr(video, 'default_thumbnail', None),
        final_thumbnail_url=(
            f"/api/videos/{video.video_id}/thumbnails/{Path(video.final_thumbnail_path).name}"
            if getattr(video, 'final_thumbnail_path', None) else None
        ),
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

    stem = Path(video.file_path).stem
    candidates = [
        f"storage/output/{video_id}/{stem}_{resolution}.mp4",
        f"storage/output/{video_id}/{resolution}.mp4",
        video.file_path,
    ]
    video_path = next((p for p in candidates if os.path.exists(p)), None)
    if not video_path:
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

    thumbnail_path = f"storage/output/{video_id}/{thumbnail_name}"
    if not os.path.exists(thumbnail_path):
        raise HTTPException(404, "Thumbnail not found")

    return FileResponse(thumbnail_path, media_type="image/jpeg", filename=thumbnail_name)


@router.delete("/videos/{video_id}", status_code=204)
async def delete_video(
    video_id: str,
    video_service: VideoService = Depends(get_video_service),
):
    """Delete a video and its associated processing job."""
    deleted = await video_service.delete_video(video_id)
    if not deleted:
        raise HTTPException(404, f"Video {video_id} not found")


@router.patch("/videos/{video_id}/pin", response_model=VideoDetailResponse)
async def pin_video(
    video_id: str,
    video_service: VideoService = Depends(get_video_service),
):
    """Toggle the pinned state of a video."""
    video = await video_service.toggle_pin(video_id)
    if not video:
        raise HTTPException(404, f"Video {video_id} not found")

    job = await video_service.get_job_by_video_id(video_id)
    if not job:
        raise HTTPException(
            404, f"No processing job found for video {video_id}")

    return _build_response(video, job)


@router.post("/videos/{video_id}/thumbnail-config", response_model=ThumbnailConfigResponse)
async def set_thumbnail_config(
    video_id: str,
    body: ThumbnailConfigRequest,
    video_service: VideoService = Depends(get_video_service),
):
    """
    Select a default thumbnail and apply a custom title overlay.

    1. Validates title length (≤ 30 chars — also enforced by schema)
    2. Resolves the source thumbnail from the job result
    3. Applies FFmpeg drawtext overlay
    4. Saves final_thumbnail.jpg to the video output directory
    5. Persists video_title, default_thumbnail, final_thumbnail_path to DB
    """
    video = await video_service.get_video_by_id(video_id)
    if not video:
        raise HTTPException(404, f"Video {video_id} not found")

    job = await video_service.get_job_by_video_id(video_id)
    if not job or job.status != JobStatus.DONE:
        raise HTTPException(400, "Video processing is not complete yet")

    # Resolve source thumbnail path from job result
    thumbnails: list = job.result.get("thumbnails", []) if job.result else []
    pct = THUMBNAIL_KEY_MAP.get(body.default_thumbnail)
    if pct is None:
        raise HTTPException(
            400, f"Invalid thumbnail key: {body.default_thumbnail}")

    # Find the thumbnail whose filename contains the matching percentage
    source_thumb = next(
        (t for t in thumbnails if f"_thumb_{pct}pct" in t),
        thumbnails[0] if thumbnails else None,
    )
    if not source_thumb or not os.path.exists(source_thumb):
        raise HTTPException(404, "Source thumbnail file not found on disk")

    output_dir = f"storage/output/{video_id}"
    os.makedirs(output_dir, exist_ok=True)
    final_path = os.path.join(output_dir, "final_thumbnail.jpg")

    try:
        apply_text_overlay(source_thumb, final_path, body.video_title)
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(422, str(exc))

    # Persist to DB
    await video_service.update_thumbnail_config(
        video_id=video_id,
        video_title=body.video_title,
        default_thumbnail=body.default_thumbnail,
        final_thumbnail_path=final_path,
    )

    return ThumbnailConfigResponse(
        video_id=video_id,
        video_title=body.video_title,
        default_thumbnail=body.default_thumbnail,
        final_thumbnail_url=f"/api/videos/{video_id}/thumbnails/final_thumbnail.jpg",
    )
