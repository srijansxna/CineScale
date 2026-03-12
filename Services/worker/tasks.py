from .celery_app import celery_app
from .job_status import set_status, update_progress
from transcoder.metadata import extract_metadata
from transcoder.transcode import transcode_video
from transcoder.thumbnails import generate_thumbnails_by_percentage
import logging
import os

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3)
def process_video(self, job: dict):
    """
    Complete video processing workflow.
    
    Workflow:
    1. Extract metadata
    2. Transcode video (360p, 720p, 1080p)
    3. Generate thumbnails (10%, 50%, 90%)
    4. Update job status
    
    Args:
        job: Dictionary containing:
            - job_id: Unique job identifier
            - input_path: Path to input video file
            - output_dir: Directory for output files
            - resolutions: Optional list of resolutions (default: ["360p", "720p", "1080p"])
            - thumbnail_percentages: Optional list of percentages (default: [10, 50, 90])
    """
    job_id = job["job_id"]
    input_path = job["input_path"]
    output_dir = job["output_dir"]
    resolutions = job.get("resolutions", ["360p", "720p", "1080p"])
    thumbnail_percentages = job.get("thumbnail_percentages", [10, 50, 90])
    
    logger.info(f"Starting video processing job: {job_id}")
    
    try:
        # Initialize job status
        set_status(job_id, "PROCESSING", {
            "progress": 0,
            "step": "initializing"
        })
        
        # Validate input file
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input video not found: {input_path}")
        
        # Step 1: Extract metadata
        logger.info(f"[{job_id}] Step 1/4: Extracting metadata")
        update_progress(job_id, 10, "extracting_metadata")
        
        metadata = extract_metadata(input_path)
        logger.info(f"[{job_id}] Metadata extracted: {metadata['resolution']} @ {metadata['fps']:.2f}fps")
        
        # Step 2: Transcode video
        logger.info(f"[{job_id}] Step 2/4: Transcoding to {len(resolutions)} resolutions")
        update_progress(job_id, 25, "transcoding")
        
        transcoded_files = transcode_video(
            input_path,
            output_dir,
            resolutions=resolutions
        )
        logger.info(f"[{job_id}] Transcoded {len(transcoded_files)} files")
        
        # Step 3: Generate thumbnails
        logger.info(f"[{job_id}] Step 3/4: Generating thumbnails")
        update_progress(job_id, 80, "generating_thumbnails")
        
        thumbnails = generate_thumbnails_by_percentage(
            input_path,
            output_dir,
            percentages=thumbnail_percentages
        )
        logger.info(f"[{job_id}] Generated {len(thumbnails)} thumbnails")
        
        # Step 4: Complete
        logger.info(f"[{job_id}] Step 4/4: Finalizing")
        update_progress(job_id, 95, "finalizing")
        
        # Build result
        result = {
            "metadata": metadata,
            "transcoded_files": transcoded_files,
            "thumbnails": thumbnails,
            "input_file": input_path,
            "output_directory": output_dir
        }
        
        # Mark as complete
        set_status(job_id, "COMPLETED", {
            "progress": 100,
            "result": result
        })
        
        logger.info(f"[{job_id}] Video processing completed successfully")
        return result
        
    except Exception as e:
        retries = self.request.retries
        logger.error(f"[{job_id}] Processing failed (attempt {retries + 1}): {str(e)}")
        
        set_status(job_id, "FAILED", {
            "error": str(e),
            "retries": retries,
            "max_retries": self.max_retries
        })
        
        # Retry with exponential backoff
        if retries < self.max_retries:
            countdown = 2 ** retries
            logger.info(f"[{job_id}] Retrying in {countdown} seconds...")
            raise self.retry(exc=e, countdown=countdown)
        else:
            logger.error(f"[{job_id}] Max retries reached, job failed permanently")
            raise


@celery_app.task
def process_video_simple(job_id: str, input_path: str, output_dir: str):
    """
    Simplified task signature for easier invocation.
    
    Args:
        job_id: Unique job identifier
        input_path: Path to input video file
        output_dir: Directory for output files
    """
    job = {
        "job_id": job_id,
        "input_path": input_path,
        "output_dir": output_dir
    }
    return process_video(job)
