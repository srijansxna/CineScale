import time

from job_status import set_status, get_status
from tasks import process_video

JOB_ID = "test"

def run_test():
    print("=== DAY 3 PIPELINE TEST START ===")

    # 1. Mark job as pending
    print("[TEST] Setting job status to PENDING")
    set_status(JOB_ID, "PENDING")

    # 2. Enqueue job
    print("[TEST] Sending job to Celery worker")
    result = process_video.delay(JOB_ID)
    print(f"[TEST] Task ID: {result.id}")

    # 3. Poll status
    print("[TEST] Waiting for job to finish...\n")
    while True:
        status = get_status(JOB_ID)

        if not status:
            print("[TEST] Status not found yet")
        else:
            print(f"[TEST] Current status: {status}")

            if status["status"] in ("DONE", "FAILED"):
                break

        time.sleep(1)

    print("\n=== FINAL RESULT ===")
    print(status)
    print("=== DAY 3 PIPELINE TEST END ===")


if __name__ == "__main__":
    run_test()
