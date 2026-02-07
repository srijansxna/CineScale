from celery_app import celery_app
from job_status import set_status

@celery_app.task(bind=True, max_retries=3)
def process_video(self, job_id):
    try:
        set_status(job_id, "PROCESSING")

        print(f"[WORKER] Working on {job_id}")

        # simulate failure
        if job_id == "fail":
            raise Exception("Simulated failure")

        set_status(job_id, "DONE")

    except Exception as e:
        retries = self.request.retries
        set_status(job_id, "FAILED", {"retries": retries})

        countdown = 2 ** retries
        raise self.retry(exc=e, countdown=countdown)
