#!/usr/bin/env python3
"""
Test script for Celery worker video processing.
"""
import sys
import os
import time
import uuid

# Ensure we can import from Services
sys.path.insert(0, os.path.dirname(__file__))

from Services.worker.tasks import process_video
from Services.worker.job_status import get_status

def main():
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
    
    print(f"Submitting video processing job: {job_id}")
    print(f"Input: {job['input_path']}")
    print(f"Output: {job['output_dir']}")
    print(f"Resolutions: {', '.join(job['resolutions'])}")
    print(f"Thumbnails: {', '.join(map(str, job['thumbnail_percentages']))}%")
    print("\n" + "="*60)
    
    # Submit job to Celery
    task = process_video.delay(job)
    print(f"Task ID: {task.id}")
    print(f"Job ID: {job_id}")
    print("\nMonitoring job status...")
    print("="*60)
    
    # Monitor job status
    last_progress = -1
    while True:
        status_data = get_status(job_id)
        
        if status_data:
            status = status_data.get("status")
            progress = status_data.get("progress", 0)
            step = status_data.get("step", "unknown")
            
            if progress != last_progress:
                print(f"[{status}] {progress}% - {step}")
                last_progress = progress
            
            if status == "COMPLETED":
                print("\n" + "="*60)
                print("JOB COMPLETED SUCCESSFULLY!")
                print("="*60)
                
                result = status_data.get("result", {})
                print(f"\nMetadata:")
                metadata = result.get("metadata", {})
                print(f"  Duration: {metadata.get('duration', 0):.2f}s")
                print(f"  Resolution: {metadata.get('resolution', 'N/A')}")
                print(f"  FPS: {metadata.get('fps', 0):.2f}")
                print(f"  Codec: {metadata.get('codec', 'N/A')}")
                
                print(f"\nTranscoded Files:")
                for res, path in result.get("transcoded_files", {}).items():
                    print(f"  {res}: {path}")
                
                print(f"\nThumbnails:")
                for thumb in result.get("thumbnails", []):
                    print(f"  {thumb}")
                
                break
            
            elif status == "FAILED":
                print("\n" + "="*60)
                print("JOB FAILED!")
                print("="*60)
                error = status_data.get("error", "Unknown error")
                print(f"Error: {error}")
                break
        
        time.sleep(2)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
