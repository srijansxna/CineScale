import subprocess
import sys
from services.api.core.jobs import jobs
from services.api.core.states import JobStatus


def process_video(job_id: str, input_path: str):
    try:
        jobs[job_id]["status"] = JobStatus.PROCESSING

        subprocess.run(
            [
                sys.executable,  # ✅ uses venv Python
                "services/api/transcoder.py",
                input_path,
                "storage/processed"
            ],
            check=True
        )

        jobs[job_id]["status"] = JobStatus.DONE

    except Exception as e:
        print("Worker failed:", e)
        jobs[job_id]["status"] = JobStatus.FAILED
