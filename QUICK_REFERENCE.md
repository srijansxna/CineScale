# CineScale Worker - Quick Reference

## Start Everything

```bash
# Terminal 1: Start Redis
docker-compose up redis

# Terminal 2: Start Worker
start_worker.bat

# Terminal 3: Test
python test_worker_simple.py
```

## Check Status

```bash
# Check dependencies
python check_setup.py

# Check if worker is running
python test_worker_simple.py
```

## Submit Job (Python)

```python
from Services.worker.tasks import process_video

job = {
    "job_id": "my_job_123",
    "input_path": "input/video.mp4",
    "output_dir": "output"
}

task = process_video.delay(job)
```

## Check Job Status (Python)

```python
from Services.worker.job_status import get_status

status = get_status("my_job_123")
print(f"{status['status']}: {status['progress']}%")
```

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Start Redis only
docker-compose up redis

# Start Redis in background
docker-compose up -d redis

# Stop Redis
docker-compose down

# View Redis logs
docker-compose logs redis

# Check Redis is running
docker ps
```

## File Locations

- Worker code: `Services/worker/`
- Transcoder code: `Services/transcoder/`
- Input videos: `input/`
- Output files: `output/`
- Test scripts: `test_*.py`

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Celery not found | `pip install -r requirements.txt` |
| Redis not accessible | `docker-compose up redis` |
| Import errors | Run from project root: `cd D:\Cinescale\CineScale` |
| FFmpeg not found | Install FFmpeg and add to PATH |
| Worker won't start | Check Redis is running first |

## Output Files

After processing `input/video.mp4`:

```
output/
├── video_360p.mp4
├── video_720p.mp4
├── video_1080p.mp4
├── video_thumb_10pct.jpg
├── video_thumb_50pct.jpg
└── video_thumb_90pct.jpg
```

## Job Status Values

- `PENDING` - Queued, not started
- `PROCESSING` - Currently running
- `COMPLETED` - Finished successfully
- `FAILED` - Error occurred

## Environment Variables

```bash
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_BROKER_DB=0
REDIS_BACKEND_DB=1
REDIS_STATUS_DB=2
```

## Need Help?

1. Check `SETUP_INSTRUCTIONS.md` for detailed setup
2. Check `WORKER_SERVICE.md` for full documentation
3. Check `WORKER_COMPLETE.md` for implementation details
4. Run `python check_setup.py` to diagnose issues
