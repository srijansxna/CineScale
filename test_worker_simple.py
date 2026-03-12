#!/usr/bin/env python3
"""
Simple test for Celery worker - tests just the worker components.
"""
import sys
import os
import time
import uuid

# Ensure we can import from Services
sys.path.insert(0, os.path.dirname(__file__))

print("Testing Celery Worker Setup...")
print("=" * 60)

# Test 1: Import Celery
try:
    from Services.worker.celery_app import celery_app
    print("✓ Celery app imported successfully")
except Exception as e:
    print(f"✗ Failed to import Celery app: {e}")
    sys.exit(1)

# Test 2: Import tasks
try:
    from Services.worker.tasks import process_video
    print("✓ Tasks imported successfully")
except Exception as e:
    print(f"✗ Failed to import tasks: {e}")
    sys.exit(1)

# Test 3: Import job status
try:
    from Services.worker.job_status import get_status, set_status
    print("✓ Job status module imported successfully")
except Exception as e:
    print(f"✗ Failed to import job status: {e}")
    sys.exit(1)

# Test 4: Check Redis connection
try:
    import redis
    r = redis.Redis(host='localhost', port=6379, db=2)
    r.ping()
    print("✓ Redis connection successful")
except Exception as e:
    print(f"✗ Redis connection failed: {e}")
    print("\nMake sure Redis is running:")
    print("  docker-compose up redis")
    sys.exit(1)

# Test 5: Check if worker is running
try:
    inspect = celery_app.control.inspect()
    active_workers = inspect.active()
    
    if active_workers:
        print(f"✓ Worker is running: {list(active_workers.keys())}")
        worker_running = True
    else:
        print("⚠ No workers detected")
        print("\nStart the worker in another terminal:")
        print("  start_worker.bat")
        worker_running = False
except Exception as e:
    print(f"⚠ Could not check worker status: {e}")
    worker_running = False

print("\n" + "=" * 60)

if worker_running:
    print("✓ All checks passed! Ready to submit jobs.")
    print("\nSubmitting a test job...")
    
    # Generate unique job ID
    job_id = f"job_{uuid.uuid4().hex[:8]}"
    
    # Job configuration
    job = {
        "job_id": job_id,
        "input_path": "input/input.mp4",
        "output_dir": "output",
        "resolutions": ["360p", "720p", "1080p"],
        "thumbnail_percentages": [10, 50, 90]
    }
    
    print(f"\nJob ID: {job_id}")
    print(f"Input: {job['input_path']}")
    
    # Submit job
    task = process_video.delay(job)
    print(f"Task ID: {task.id}")
    print("\nMonitoring job status (Ctrl+C to stop)...")
    print("=" * 60)
    
    # Monitor progress
    last_status = None
    try:
        while True:
            status_data = get_status(job_id)
            
            if status_data:
                status = status_data.get("status")
                progress = status_data.get("progress", 0)
                step = status_data.get("step", "unknown")
                
                current = f"{status}:{progress}:{step}"
                if current != last_status:
                    print(f"[{status}] {progress}% - {step}")
                    last_status = current
                
                if status in ["COMPLETED", "FAILED"]:
                    print("\n" + "=" * 60)
                    if status == "COMPLETED":
                        print("✓ JOB COMPLETED!")
                        result = status_data.get("result", {})
                        print(f"\nTranscoded files: {len(result.get('transcoded_files', {}))}")
                        print(f"Thumbnails: {len(result.get('thumbnails', []))}")
                    else:
                        print("✗ JOB FAILED!")
                        print(f"Error: {status_data.get('error', 'Unknown')}")
                    break
            
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")
        print(f"Job {job_id} is still running in the background.")
else:
    print("⚠ Worker is not running.")
    print("\nTo start the worker:")
    print("  1. Open a new terminal")
    print("  2. Run: start_worker.bat")
    print("  3. Then run this test again")

print("\nDone!")
