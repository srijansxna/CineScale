import time
from services.api.core.jobs import jobs
from services.api.core.states import JobStatus

def process_video(job_id: str):
    try:
        jobs[job_id]["status"] = JobStatus.PROCESSING
        time.sleep(5)  # simulate processing
        jobs[job_id]["status"] = JobStatus.DONE
    except Exception:
        jobs[job_id]["status"] = JobStatus.FAILED
