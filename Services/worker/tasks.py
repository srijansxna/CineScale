from celery_app import celery_app
from job_status import set_status
from transcoder.pipeline import run_pipeline


@celery_app.task(bind=True, max_retries=3)
def process_video(self, job: dict):
    """
    job = {
        "job_id": str,
        "input_path": str,
        "output_dir": str
    }
    """
    job_id = job["job_id"]

    try:
        set_status(job_id, "PROCESSING")

        result = run_pipeline(
            video_path=job["input_path"],
            output_dir=job["output_dir"]
        )

        set_status(job_id, "DONE", result)

    except Exception as e:
        retries = self.request.retries
        set_status(job_id, "FAILED", {"retries": retries})
        raise self.retry(exc=e, countdown=2 ** retries)
