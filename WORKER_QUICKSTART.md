# Worker Service Quick Start Guide

## Prerequisites

1. Redis running (via Docker or locally)
2. FFmpeg and FFprobe installed
3. Python dependencies installed

## Step 1: Start Redis

Using Docker Compose:
```bash
docker-compose up redis
```

Or manually:
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

## Step 2: Start the Worker

### Windows:
```bash
start_worker.bat
```

### Linux/Mac:
```bash
chmod +x start_worker.sh
./start_worker.sh
```

### Manual:
```bash
cd Services/worker
celery -A celery_app worker --loglevel=info
```

## Step 3: Submit a Test Job

In a new terminal:
```bash
python test_worker.py
```

You should see:
- Job submission confirmation
- Real-time progress updates
- Final results with file paths

## Expected Output

```
Submitting video processing job: job_abc12345
Input: input/input.mp4
Output: output
Resolutions: 360p, 720p, 1080p
Thumbnails: 10, 50, 90%

============================================================
Task ID: 1234-5678-90ab-cdef
Job ID: job_abc12345

Monitoring job status...
============================================================
[PROCESSING] 0% - initializing
[PROCESSING] 10% - extracting_metadata
[PROCESSING] 25% - transcoding
[PROCESSING] 80% - generating_thumbnails
[PROCESSING] 95% - finalizing
[COMPLETED] 100% - complete

============================================================
JOB COMPLETED SUCCESSFULLY!
============================================================

Metadata:
  Duration: 120.50s
  Resolution: 1920x1080
  FPS: 30.00
  Codec: h264

Transcoded Files:
  360p: output/input_360p.mp4
  720p: output/input_720p.mp4
  1080p: output/input_1080p.mp4

Thumbnails:
  output/input_thumb_10pct.jpg
  output/input_thumb_50pct.jpg
  output/input_thumb_90pct.jpg
```

## Troubleshooting

### Worker won't start
- Check Redis is running: `redis-cli ping` (should return "PONG")
- Verify Python path includes Services directory
- Check for port conflicts on 6379

### Job fails immediately
- Verify input video file exists
- Check FFmpeg is installed: `ffmpeg -version`
- Check worker logs for detailed error messages

### No progress updates
- Ensure Redis STATUS_DB is accessible
- Check Redis connection in job_status.py
- Verify REDIS_HOST environment variable

## Environment Variables

```bash
# Redis Configuration
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_BROKER_DB=0
export REDIS_BACKEND_DB=1
export REDIS_STATUS_DB=2
```

## Next Steps

- Integrate with API service for job submission
- Add webhook notifications for job completion
- Implement job priority queues
- Add support for custom encoding parameters
