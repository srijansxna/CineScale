import time
from job_status import set_status, get_status
from tasks import process_video

JOB = {
    "job_id": "day4-demo",
    "input_path": "samples/demo.mp4",
    "output_dir": "outputs/day4-demo"
}


def run_test():
    print("=== DAY 4 TEST START ===")

    set_status(JOB["job_id"], "PENDING")

    result = process_video.delay(JOB)
    print(f"[TEST] Task ID: {result.id}")

    while True:
        status = get_status(JOB["job_id"])
        print("[TEST] Status:", status)

        if status and status["status"] in ("DONE", "FAILED"):
            break

        time.sleep(1)

    print("=== DAY 4 TEST END ===")


if __name__ == "__main__":
    run_test()
