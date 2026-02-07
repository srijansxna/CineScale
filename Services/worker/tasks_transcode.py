from celery_app import celery_app
from job_status import set_status
from transcoder.transcode import transcode


@celery_app.task(bind=True, max_retries=1)
def transcode_task(self, job: dict):
    job_id = job["job_id"]

    try:
        set_status(job_id, "PROCESSING_TRANSCODE")

        renditions = transcode(
            job["input_path"],
            job["output_dir"]
        )

        set_status(job_id, "DONE", {
            "renditions": renditions
        })

    except Exception as e:
        set_status(job_id, "FAILED_TRANSCODE")
        raise self.retry(exc=e, countdown=5)
