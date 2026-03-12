# Celery Worker Service for Video Processing

## Overview

The Celery worker service handles asynchronous video processing tasks including metadata extraction, transcoding, and thumbnail generation.

## Architecture

- **Broker**: Redis (for task queue)
- **Backend**: Redis (for result storage)
- **Status Store**: Redis (for job status tracking)

## Workflow

1. **Receive Job**: Accept video processing job with input path and output directory
2. **Extract Metadata**: Get video duration, codec, fps, resolution, bitrate
3. **Transcode Video**: Convert to 360p, 720p, and 1080p resolutions
4. **Generate Thumbnails**: Extract frames at 10%, 50%, and 90% positions
5. **Update Status**: Track progress and final results in Redis

## Job Status States

- `PENDING`: Job queued but not started
- `PROCESSING`: Job is being processed
- `COMPLETED`: Job finished successfully
- `FAILED`: Job failed (with retry information)

## Configuration

Environment variables:
```bash
REDIS_HOST=localhost          # Redis server host
REDIS_PORT=6379              # Redis server port
REDIS_BROKER_DB=0            # Redis DB for Celery broker
REDIS_BACKEND_DB=1           # Redis DB for Celery backend
REDIS_STATUS_DB=2            # Redis DB for job status
```

## Usage

### Starting the Worker

```bash
# Using Docker Compose
docker-compose up worker

# Manual start
celery -A Services.worker.celery_app worker --loglevel=info
```

### Submitting a Job

```python
from Services.worker.tasks import process_video

job = {
    "job_id": "unique_job_id",
    "input_path": "path/to/video.mp4",
    "output_dir": "path/to/output",
    "resolutions": ["360p", "720p", "1080p"],  # Optional
    "thumbnail_percentages": [10, 50, 90]      # Optional
}

task = process_video.delay(job)
```

### Checking Job Status

```python
from Services.worker.job_status import get_status

status = get_status("unique_job_id")
print(status)
# {
#   "status": "PROCESSING",
#   "progress": 45,
#   "step": "transcoding"
# }
```

## Testing

Run the test script:
```bash
python test_worker.py
```

This will:
1. Submit a test job
2. Monitor progress in real-time
3. Display results when complete

## Output Structure

Completed job result:
```json
{
  "status": "COMPLETED",
  "progress": 100,
  "result": {
    "metadata": {
      "duration": 120.5,
      "codec": "h264",
      "fps": 30.0,
      "resolution": "1920x1080",
      "bitrate": 5000000
    },
    "transcoded_files": {
      "360p": "output/video_360p.mp4",
      "720p": "output/video_720p.mp4",
      "1080p": "output/video_1080p.mp4"
    },
    "thumbnails": [
      "output/video_thumb_10pct.jpg",
      "output/video_thumb_50pct.jpg",
      "output/video_thumb_90pct.jpg"
    ]
  }
}
```

## Error Handling

- Automatic retry with exponential backoff (max 3 retries)
- Detailed error messages in status
- Retry count tracking
- Graceful failure handling

## Monitoring

View worker logs:
```bash
# Docker
docker-compose logs -f worker

# Manual
# Logs appear in terminal where worker is running
```

## Dependencies

- celery
- redis
- ffmpeg (system dependency)
- ffprobe (system dependency)
