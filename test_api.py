#!/usr/bin/env python3
"""
Full integration test for CineScale API.
Tests: health, upload, job status, video detail endpoints.
"""
import sys
import time
import json
import requests

BASE_URL = "http://localhost:8000"
INPUT_VIDEO = "input/input.mp4"
PASS = "\033[92m✓\033[0m"
FAIL = "\033[91m✗\033[0m"
INFO = "\033[94m→\033[0m"

results = []

def check(label, condition, detail=""):
    status = PASS if condition else FAIL
    print(f"  {status} {label}" + (f" — {detail}" if detail else ""))
    results.append((label, condition))
    return condition


def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


# ─── TEST 1: Health Check ─────────────────────────────────────────────────────
section("TEST 1: Health & Root Endpoints")

try:
    r = requests.get(f"{BASE_URL}/health", timeout=5)
    check("GET /health returns 200", r.status_code == 200)
    check("Status is 'ok'", r.json().get("status") == "ok", r.json().get("status"))
except Exception as e:
    check("GET /health reachable", False, str(e))
    print("\n  API is not running. Start it with: docker-compose up api")
    sys.exit(1)

try:
    r = requests.get(f"{BASE_URL}/", timeout=5)
    check("GET / returns 200", r.status_code == 200)
    check("Docs link present", "/docs" in r.json().get("docs", ""))
except Exception as e:
    check("GET / reachable", False, str(e))

try:
    r = requests.get(f"{BASE_URL}/docs", timeout=5)
    check("GET /docs (Swagger UI) returns 200", r.status_code == 200)
except Exception as e:
    check("GET /docs reachable", False, str(e))


# ─── TEST 2: Upload Endpoint ──────────────────────────────────────────────────
section("TEST 2: POST /api/upload")

job_id = None
video_id = None

try:
    with open(INPUT_VIDEO, "rb") as f:
        r = requests.post(
            f"{BASE_URL}/api/upload",
            files={"file": ("input.mp4", f, "video/mp4")},
            timeout=30
        )

    check("POST /api/upload returns 200", r.status_code == 200, f"got {r.status_code}")

    if r.status_code == 200:
        data = r.json()
        print(f"\n  {INFO} Response:")
        print(f"      {json.dumps(data, indent=6, default=str)}")

        job_id  = data.get("job_id")
        video_id = data.get("video_id")

        check("Response has job_id",   bool(job_id))
        check("Response has video_id", bool(video_id))
        check("Response has filename", bool(data.get("filename")))
        check("Response has file_size", isinstance(data.get("file_size"), int))
        check("Initial status is PENDING", data.get("status") == "PENDING", data.get("status"))
    else:
        print(f"\n  Response: {r.text}")

except FileNotFoundError:
    check("Input video exists", False, f"{INPUT_VIDEO} not found")
except Exception as e:
    check("POST /api/upload", False, str(e))


# ─── TEST 3: Invalid Upload ───────────────────────────────────────────────────
section("TEST 3: Upload Validation")

try:
    r = requests.post(
        f"{BASE_URL}/api/upload",
        files={"file": ("test.txt", b"not a video", "text/plain")},
        timeout=10
    )
    check("Rejects invalid file type (txt)", r.status_code == 400, f"got {r.status_code}")
except Exception as e:
    check("Upload validation", False, str(e))


# ─── TEST 4: Job Status ───────────────────────────────────────────────────────
section("TEST 4: GET /api/job/{job_id}")

if job_id:
    try:
        r = requests.get(f"{BASE_URL}/api/job/{job_id}", timeout=5)
        check("GET /api/job/{job_id} returns 200", r.status_code == 200, f"got {r.status_code}")

        if r.status_code == 200:
            data = r.json()
            print(f"\n  {INFO} Response:")
            print(f"      {json.dumps(data, indent=6, default=str)}")

            check("Has job_id",   data.get("job_id") == job_id)
            check("Has video_id", data.get("video_id") == video_id)
            check("Has status",   data.get("status") in ["PENDING", "PROCESSING", "DONE", "FAILED"])
            check("Has progress", isinstance(data.get("progress"), int))
    except Exception as e:
        check("GET /api/job/{job_id}", False, str(e))

    # 404 for unknown job
    try:
        r = requests.get(f"{BASE_URL}/api/job/nonexistent-job-id", timeout=5)
        check("Returns 404 for unknown job_id", r.status_code == 404, f"got {r.status_code}")
    except Exception as e:
        check("404 for unknown job", False, str(e))
else:
    print("  Skipped — no job_id from upload")


# ─── TEST 5: Video Detail ─────────────────────────────────────────────────────
section("TEST 5: GET /api/videos/{video_id}")

if video_id:
    try:
        r = requests.get(f"{BASE_URL}/api/videos/{video_id}", timeout=5)
        check("GET /api/videos/{video_id} returns 200", r.status_code == 200, f"got {r.status_code}")

        if r.status_code == 200:
            data = r.json()
            print(f"\n  {INFO} Response:")
            print(f"      {json.dumps(data, indent=6, default=str)}")

            check("Has video_id",  data.get("video_id") == video_id)
            check("Has filename",  bool(data.get("filename")))
            check("Has processing status", bool(data.get("processing", {}).get("status")))
    except Exception as e:
        check("GET /api/videos/{video_id}", False, str(e))

    # 404 for unknown video
    try:
        r = requests.get(f"{BASE_URL}/api/videos/nonexistent-video-id", timeout=5)
        check("Returns 404 for unknown video_id", r.status_code == 404, f"got {r.status_code}")
    except Exception as e:
        check("404 for unknown video", False, str(e))
else:
    print("  Skipped — no video_id from upload")


# ─── TEST 6: Job Progress Polling ────────────────────────────────────────────
section("TEST 6: Job Progress Polling (30s)")

if job_id:
    print(f"  {INFO} Polling job {job_id} for up to 30 seconds...\n")
    deadline = time.time() + 30
    last_progress = -1

    while time.time() < deadline:
        try:
            r = requests.get(f"{BASE_URL}/api/job/{job_id}", timeout=5)
            if r.status_code == 200:
                data = r.json()
                status   = data.get("status")
                progress = data.get("progress", 0)

                if progress != last_progress:
                    print(f"  {INFO} [{status}] {progress}%")
                    last_progress = progress

                if status in ("DONE", "FAILED"):
                    break
        except Exception:
            pass
        time.sleep(2)

    final = requests.get(f"{BASE_URL}/api/job/{job_id}", timeout=5).json()
    final_status = final.get("status")
    check("Job reached terminal state or is processing",
          final_status in ("DONE", "FAILED", "PROCESSING", "PENDING"),
          final_status)
    if final_status == "DONE":
        check("Job completed successfully", True, "DONE")
    elif final_status == "FAILED":
        check("Job failed (check worker logs)", False, final.get("error", ""))
    elif final_status == "PENDING":
        check("Job queued — worker not running yet", True, "start worker to process")
else:
    print("  Skipped — no job_id from upload")


# ─── SUMMARY ─────────────────────────────────────────────────────────────────
section("Test Summary")

passed = sum(1 for _, ok in results if ok)
failed = sum(1 for _, ok in results if not ok)
total  = len(results)

for label, ok in results:
    print(f"  {PASS if ok else FAIL} {label}")

print(f"\n  Passed: {passed}/{total}")

if failed == 0:
    print("\n  \033[92mAll tests passed! API is working correctly.\033[0m")
    sys.exit(0)
else:
    print(f"\n  \033[91m{failed} test(s) failed.\033[0m")
    sys.exit(1)
