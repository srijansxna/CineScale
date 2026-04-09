import json
import logging
import os
from datetime import datetime, timezone

import psycopg2

from .celery_app import celery_app
from .job_status import set_status, update_progress
from services.transcoder.metadata import extract_metadata
from services.transcoder.transcode import transcode_video
from services.transcoder.thumbnails import generate_thumbnails_by_percentage

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@postgres:5432/cinescale",
)


def _pg_conn():
    """Return a synchronous psycopg2 connection parsed from DATABASE_URL."""
    # Strip asyncpg driver prefix so psycopg2 can parse it
    url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    return psycopg2.connect(url)


def _db_update_job(job_id: str, status: str, progress: int, result: dict = None, error: str = None):
    """Synchronously update the processing_jobs row in Postgres."""
    try:
        conn = _pg_conn()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE processing_jobs
               SET status     = %s,
                   progress   = %s,
                   result     = %s,
                   error      = %s,
                   updated_at = %s
             WHERE job_id     = %s
            """,
            (
                status,
                progress,
                json.dumps(result) if result else None,
                error,
                datetime.now(timezone.utc),
                job_id,
            ),
        )
        conn.commit()
        cur.close()
        conn.close()
        logger.debug(f"[{job_id}] DB updated → {status} {progress}%")
    except Exception as exc:
        logger.error(f"[{job_id}] Failed to update DB: {exc}")


@celery_app.task(bind=True, max_retries=3)
def process_video(self, job: dict):
    job_id = job["job_id"]
    input_path = job["input_path"]
    output_dir = job["output_dir"]
    resolutions = job.get("resolutions", ["360p", "720p", "1080p"])
    thumbnail_percentages = job.get("thumbnail_percentages", [10, 50, 90])

    logger.info(f"Starting video processing job: {job_id}")

    try:
        # Mark PROCESSING in both Redis and Postgres
        set_status(job_id, "PROCESSING", {
                   "progress": 0, "step": "initializing"})
        _db_update_job(job_id, "PROCESSING", 0)

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input video not found: {input_path}")

        # Step 1 — metadata
        logger.info(f"[{job_id}] Step 1/4: Extracting metadata")
        update_progress(job_id, 10, "extracting_metadata")
        _db_update_job(job_id, "PROCESSING", 10)
        metadata = extract_metadata(input_path)
        logger.info(
            f"[{job_id}] Metadata: {metadata.get('resolution')} @ {metadata.get('fps')}fps")

        # Step 2 — transcode
        logger.info(f"[{job_id}] Step 2/4: Transcoding")
        update_progress(job_id, 25, "transcoding")
        _db_update_job(job_id, "PROCESSING", 25)
        transcoded_files = transcode_video(
            input_path, output_dir, resolutions=resolutions)
        logger.info(f"[{job_id}] Transcoded {len(transcoded_files)} files")

        # Step 3 — thumbnails
        logger.info(f"[{job_id}] Step 3/4: Generating thumbnails")
        update_progress(job_id, 80, "generating_thumbnails")
        _db_update_job(job_id, "PROCESSING", 80)
        thumbnails = generate_thumbnails_by_percentage(
            input_path, output_dir, percentages=thumbnail_percentages
        )
        logger.info(f"[{job_id}] Generated {len(thumbnails)} thumbnails")

        # Step 4 — finalise
        logger.info(f"[{job_id}] Step 4/4: Finalizing")
        update_progress(job_id, 95, "finalizing")
        _db_update_job(job_id, "PROCESSING", 95)

        result = {
            "metadata": metadata,
            "variants": [
                {
                    "resolution": res,
                    "width":  {"360p": 640,  "720p": 1280, "1080p": 1920}.get(res, 0),
                    "height": {"360p": 360,  "720p": 720,  "1080p": 1080}.get(res, 0),
                    "file_size": os.path.getsize(path) if os.path.exists(path) else None,
                    "status": "ready",
                }
                for res, path in transcoded_files.items()
            ],
            "thumbnails": thumbnails,
        }

        # Write DONE to Redis + Postgres
        set_status(job_id, "DONE", {"progress": 100, "result": result})
        _db_update_job(job_id, "DONE", 100, result=result)

        logger.info(f"[{job_id}] Completed successfully")
        return result

    except Exception as exc:
        retries = self.request.retries
        logger.error(f"[{job_id}] Failed (attempt {retries + 1}): {exc}")

        set_status(job_id, "FAILED", {"error": str(exc)})
        _db_update_job(job_id, "FAILED", 0, error=str(exc))

        if retries < self.max_retries:
            raise self.retry(exc=exc, countdown=2 ** retries)
        raise
