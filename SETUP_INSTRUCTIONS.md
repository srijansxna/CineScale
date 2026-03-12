# CineScale Setup Instructions

## Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- celery (task queue)
- redis (Python client)
- fastapi (API framework)
- And other dependencies

## Step 2: Verify Installation

```bash
python check_setup.py
```

This will check:
- Python packages are installed
- FFmpeg and FFprobe are available
- Redis is running

## Step 3: Start Redis

Redis must be running before starting the worker.

```bash
docker-compose up redis
```

Or in detached mode:
```bash
docker-compose up -d redis
```

## Step 4: Start the Worker

```bash
start_worker.bat
```

You should see output like:
```
Starting Celery Worker...
[2026-03-13 00:00:00,000: INFO/MainProcess] Connected to redis://localhost:6379/0
[2026-03-13 00:00:00,000: INFO/MainProcess] celery@hostname ready.
```

## Step 5: Test the Worker

In a new terminal:

```bash
python test_worker.py
```

You should see:
- Job submission
- Progress updates (0% → 100%)
- Final results with file paths

## Troubleshooting

### "celery is not installed"

Install dependencies:
```bash
pip install -r requirements.txt
```

### "Redis is NOT accessible"

Start Redis:
```bash
docker-compose up redis
```

Check Redis is running:
```bash
docker ps
```

### "ModuleNotFoundError: No module named 'celery_app'"

Make sure you're running from the project root directory:
```bash
cd D:\Cinescale\CineScale
python test_worker.py
```

### "FFmpeg not found"

Install FFmpeg:
- Windows: Download from https://ffmpeg.org/download.html
- Add to PATH environment variable
- Verify: `ffmpeg -version`

### Worker starts but jobs fail

Check:
1. Input video file exists: `input/input.mp4`
2. FFmpeg is accessible: `ffmpeg -version`
3. Output directory is writable
4. Check worker logs for detailed errors

## Windows-Specific Notes

On Windows, Celery requires the `--pool=solo` flag (already included in start_worker.bat).

If you see "billiard" errors, this is normal on Windows and handled by the solo pool.

## Next Steps

Once everything works:
1. Integrate with the API service
2. Configure production settings
3. Set up monitoring and logging
4. Deploy to production environment
