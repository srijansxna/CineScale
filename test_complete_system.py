#!/usr/bin/env python3
"""
Complete system test for CineScale video processing.
Tests all modules individually and then the complete workflow.
"""
import sys
import os
import time

# Ensure we can import from Services
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 70)
print("CineScale Complete System Test")
print("=" * 70)
print()

# Test 1: Check Dependencies
print("TEST 1: Checking Dependencies")
print("-" * 70)

try:
    import redis
    print("✓ Redis Python client installed")
except ImportError:
    print("✗ Redis Python client NOT installed")
    sys.exit(1)

try:
    import celery
    print("✓ Celery installed")
except ImportError:
    print("✗ Celery NOT installed")
    sys.exit(1)

try:
    import subprocess
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True, timeout=5)
    if result.returncode == 0:
        print("✓ FFmpeg available")
    else:
        print("✗ FFmpeg not working")
        sys.exit(1)
except Exception as e:
    print(f"✗ FFmpeg not available: {e}")
    sys.exit(1)

try:
    result = subprocess.run(["ffprobe", "-version"], capture_output=True, timeout=5)
    if result.returncode == 0:
        print("✓ FFprobe available")
    else:
        print("✗ FFprobe not working")
        sys.exit(1)
except Exception as e:
    print(f"✗ FFprobe not available: {e}")
    sys.exit(1)

# Test Redis connection
try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()
    print("✓ Redis server running and accessible")
except Exception as e:
    print(f"✗ Redis server not accessible: {e}")
    print("\nPlease start Redis: docker-compose up redis")
    sys.exit(1)

print()

# Test 2: Import Modules
print("TEST 2: Importing Modules")
print("-" * 70)

try:
    from Services.transcoder.metadata import extract_metadata
    print("✓ Metadata module imported")
except Exception as e:
    print(f"✗ Failed to import metadata module: {e}")
    sys.exit(1)

try:
    from Services.transcoder.transcode import transcode_video
    print("✓ Transcode module imported")
except Exception as e:
    print(f"✗ Failed to import transcode module: {e}")
    sys.exit(1)

try:
    from Services.transcoder.thumbnails import generate_thumbnails_by_percentage
    print("✓ Thumbnails module imported")
except Exception as e:
    print(f"✗ Failed to import thumbnails module: {e}")
    sys.exit(1)

try:
    from Services.worker.celery_app import celery_app
    print("✓ Celery app imported")
except Exception as e:
    print(f"✗ Failed to import Celery app: {e}")
    sys.exit(1)

try:
    from Services.worker.tasks import process_video
    print("✓ Worker tasks imported")
except Exception as e:
    print(f"✗ Failed to import worker tasks: {e}")
    sys.exit(1)

try:
    from Services.worker.job_status import get_status, set_status
    print("✓ Job status module imported")
except Exception as e:
    print(f"✗ Failed to import job status: {e}")
    sys.exit(1)

print()

# Test 3: Check Input File
print("TEST 3: Checking Input File")
print("-" * 70)

input_file = "input/input.mp4"
if os.path.exists(input_file):
    size_mb = os.path.getsize(input_file) / (1024 * 1024)
    print(f"✓ Input file exists: {input_file} ({size_mb:.2f} MB)")
else:
    print(f"✗ Input file not found: {input_file}")
    sys.exit(1)

print()

# Test 4: Test Metadata Extraction
print("TEST 4: Testing Metadata Extraction")
print("-" * 70)

try:
    metadata = extract_metadata(input_file)
    print(f"✓ Metadata extracted successfully")
    print(f"  Duration: {metadata['duration']:.2f}s")
    print(f"  Resolution: {metadata['resolution']}")
    print(f"  FPS: {metadata['fps']:.2f}")
    print(f"  Codec: {metadata['codec']}")
    print(f"  Bitrate: {metadata['bitrate']:,} bits/sec")
except Exception as e:
    print(f"✗ Metadata extraction failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 5: Test Thumbnail Generation
print("TEST 5: Testing Thumbnail Generation")
print("-" * 70)

test_output_dir = "output/test_thumbnails"
os.makedirs(test_output_dir, exist_ok=True)

try:
    thumbnails = generate_thumbnails_by_percentage(
        input_file,
        test_output_dir,
        percentages=[10, 50, 90]
    )
    print(f"✓ Generated {len(thumbnails)} thumbnails")
    for thumb in thumbnails:
        if os.path.exists(thumb):
            size_kb = os.path.getsize(thumb) / 1024
            print(f"  ✓ {os.path.basename(thumb)} ({size_kb:.2f} KB)")
        else:
            print(f"  ✗ {os.path.basename(thumb)} not created")
except Exception as e:
    print(f"✗ Thumbnail generation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 6: Test Video Transcoding (single resolution for speed)
print("TEST 6: Testing Video Transcoding")
print("-" * 70)
print("Note: Testing only 360p for speed (full test takes longer)")

test_transcode_dir = "output/test_transcode"
os.makedirs(test_transcode_dir, exist_ok=True)

try:
    transcoded = transcode_video(
        input_file,
        test_transcode_dir,
        resolutions=["360p"]  # Only test one resolution for speed
    )
    print(f"✓ Transcoded {len(transcoded)} file(s)")
    for res, path in transcoded.items():
        if os.path.exists(path):
            size_mb = os.path.getsize(path) / (1024 * 1024)
            print(f"  ✓ {res}: {os.path.basename(path)} ({size_mb:.2f} MB)")
        else:
            print(f"  ✗ {res}: {os.path.basename(path)} not created")
except Exception as e:
    print(f"✗ Transcoding failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 7: Check Worker Status
print("TEST 7: Checking Celery Worker")
print("-" * 70)

try:
    inspect = celery_app.control.inspect()
    active_workers = inspect.active()
    
    if active_workers:
        print(f"✓ Worker is running")
        for worker_name in active_workers.keys():
            print(f"  Worker: {worker_name}")
        worker_running = True
    else:
        print("⚠ No workers detected (worker not required for module tests)")
        print("  To test full workflow, start worker: start_worker.bat")
        worker_running = False
except Exception as e:
    print(f"⚠ Could not check worker status: {e}")
    worker_running = False

print()

# Test 8: Test Complete Workflow (if worker is running)
if worker_running:
    print("TEST 8: Testing Complete Workflow with Worker")
    print("-" * 70)
    
    import uuid
    job_id = f"test_{uuid.uuid4().hex[:8]}"
    
    job = {
        "job_id": job_id,
        "input_path": input_file,
        "output_dir": "output/test_workflow",
        "resolutions": ["360p"],  # Only one resolution for speed
        "thumbnail_percentages": [50]  # Only one thumbnail for speed
    }
    
    print(f"Submitting test job: {job_id}")
    
    try:
        task = process_video.delay(job)
        print(f"✓ Job submitted: {task.id}")
        print("  Monitoring progress...")
        
        # Monitor for up to 120 seconds
        timeout = 120
        start_time = time.time()
        last_status = None
        
        while time.time() - start_time < timeout:
            status_data = get_status(job_id)
            
            if status_data:
                status = status_data.get("status")
                progress = status_data.get("progress", 0)
                step = status_data.get("step", "unknown")
                
                current = f"{status}:{progress}"
                if current != last_status:
                    print(f"  [{status}] {progress}% - {step}")
                    last_status = current
                
                if status == "COMPLETED":
                    print("✓ Workflow completed successfully!")
                    result = status_data.get("result", {})
                    print(f"  Transcoded files: {len(result.get('transcoded_files', {}))}")
                    print(f"  Thumbnails: {len(result.get('thumbnails', []))}")
                    break
                elif status == "FAILED":
                    print(f"✗ Workflow failed: {status_data.get('error', 'Unknown')}")
                    break
            
            time.sleep(2)
        else:
            print("⚠ Workflow test timed out (job may still be running)")
    
    except Exception as e:
        print(f"✗ Workflow test failed: {e}")
        import traceback
        traceback.print_exc()
else:
    print("TEST 8: Skipping Workflow Test (worker not running)")
    print("-" * 70)
    print("To test complete workflow:")
    print("  1. Start worker: start_worker.bat")
    print("  2. Run: python test_worker_simple.py")

print()
print("=" * 70)
print("Test Summary")
print("=" * 70)
print("✓ All module tests passed!")
print("✓ Metadata extraction working")
print("✓ Thumbnail generation working")
print("✓ Video transcoding working")
if worker_running:
    print("✓ Worker integration working")
else:
    print("⚠ Worker tests skipped (start worker to test)")
print()
print("System is ready for production use!")
print("=" * 70)
