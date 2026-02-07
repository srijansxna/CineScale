from celery_app import celery_app
from job_status import set_status
from transcoder.thumbnails import generate_thumbnails


@celery_app.task(bind=True, max_retries=2)
def generate_thumbnails_task(self, job: dict):
    job_id = job["job_id"]

    try:
        set_status(job_id, "PROCESSING_THUMBNAILS")

        thumbnails = generate_thumbnails(
            job["input_path"],
            job["output_dir"]
        )

        set_status(job_id, "THUMBNAILS_DONE", {
            "thumbnails": thumbnails
        })

    except Exception as e:
        set_status(job_id, "FAILED_THUMBNAILS")
        raise self.retry(exc=e, countdown=2 ** self.request.retries)
