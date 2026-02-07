from pathlib import Path
from tasks import process_video
from job_status import set_status

SAMPLES_DIR = Path("samples")
OUTPUTS_DIR = Path("outputs")


def dispatch_all():
    if not SAMPLES_DIR.exists():
        print("[DISPATCHER] samples/ folder does not exist")
        return

    videos = list(SAMPLES_DIR.glob("*.mp4"))

    if not videos:
        print("[DISPATCHER] No videos found")
        return

    for video in videos:
        job_id = video.stem  # filename without extension

        job = {
            "job_id": job_id,
            "input_path": str(video),
            "output_dir": str(OUTPUTS_DIR / job_id)
        }

        print(f"[DISPATCHER] Enqueuing job: {job_id}")

        set_status(job_id, "PENDING")
        process_video.delay(job)


if __name__ == "__main__":
    dispatch_all()
