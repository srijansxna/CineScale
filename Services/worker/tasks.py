from celery_app import celery_app

@celery_app.task
def process_video(job_id):
    print(f"[WORKER] Processing job: {job_id}")
