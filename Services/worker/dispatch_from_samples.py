from pathlib import Path
from job_status import set_status
from tasks_thumbnail import generate_thumbnails_task
from tasks_transcode import transcode_task

SAMPLES_DIR = Path("samples")
OUTPUTS_DIR = Path("outputs")


def dispatch_all():
    for video in SAMPLES_DIR.glob("*.mp4"):
        job_id = video.stem

        job = {
            "job_id": job_id,
            "input_path": str(video),
            "output_dir": str(OUTPUTS_DIR / job_id)
        }

        set_status(job_id, "PENDING")

        generate_thumbnails_task.delay(job)
        transcode_task.delay(job)

        print(f"[DISPATCH] Job enqueued: {job_id}")


if __name__ == "__main__":
    dispatch_all()
