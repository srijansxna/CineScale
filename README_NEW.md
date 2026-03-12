# CineScale - Refactored FastAPI Backend

A modular, production-ready FastAPI backend for video processing.

## Project Structure

```
services/
├── api/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Environment configuration
│   ├── routes/
│   │   ├── upload.py        # Video upload endpoints
│   │   ├── jobs.py          # Job status endpoints
│   │   └── videos.py        # Video streaming endpoints
│   ├── db/
│   │   ├── database.py      # Redis connection
│   │   └── models.py        # Data models (enums)
│   ├── schemas/
│   │   ├── video.py         # Video Pydantic schemas
│   │   └── job.py           # Job Pydantic schemas
│   └── services/
│       ├── storage.py       # File storage service
│       └── job_service.py   # Job management service
```

## Features

- ✅ Async FastAPI endpoints
- ✅ Modular service architecture
- ✅ Environment-based configuration
- ✅ Redis for job status tracking
- ✅ Docker & Docker Compose ready
- ✅ Pydantic schemas for validation
- ✅ Dependency injection pattern
- ✅ CORS middleware
- ✅ Health check endpoint

## Quick Start

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Start Redis:
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

4. Run the API:
```bash
uvicorn services.api.main:app --reload
```

5. Access the API:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

### Docker Compose

```bash
docker-compose up --build
```

This starts:
- FastAPI API server (port 8000)
- Redis (port 6379)
- Celery worker

## API Endpoints

### Upload Video
```bash
POST /api/upload
Content-Type: multipart/form-data

Response:
{
  "job_id": "uuid",
  "status": "PENDING",
  "filename": "video.mp4"
}
```

### Get Job Status
```bash
GET /api/jobs/{job_id}

Response:
{
  "job_id": "uuid",
  "status": "DONE",
  "result": {
    "metadata": {...},
    "thumbnails": [...]
  }
}
```

### Get Video Info
```bash
GET /api/videos/{job_id}

Response:
{
  "job_id": "uuid",
  "filename": "video.mp4",
  "status": "DONE",
  "metadata": {...}
}
```

### Stream Video
```bash
GET /api/videos/{job_id}/stream/{resolution}
# resolution: 240p, 360p, 720p, 1080p
```

## Configuration

Environment variables (`.env`):

```env
APP_NAME=CineScale
DEBUG=False
REDIS_HOST=localhost
REDIS_PORT=6379
STORAGE_RAW_DIR=storage/raw
STORAGE_OUTPUT_DIR=storage/output
```

## Architecture

### Service Layer
- `StorageService`: Handles file operations
- `JobService`: Manages job status in Redis

### Dependency Injection
Services are injected using FastAPI's `Depends()`:

```python
async def upload_video(
    storage: StorageService = Depends(get_storage_service)
):
    ...
```

### Configuration Management
Settings loaded from environment using Pydantic:

```python
from services.api.config import get_settings
settings = get_settings()
```

## Development

### Run Tests
```bash
pytest
```

### Format Code
```bash
black services/
```

### Type Checking
```bash
mypy services/
```

## Docker Deployment

Build and run:
```bash
docker-compose up -d
```

Scale workers:
```bash
docker-compose up -d --scale worker=3
```

View logs:
```bash
docker-compose logs -f api
```

## Next Steps

- [ ] Add database (PostgreSQL) for persistent storage
- [ ] Implement authentication/authorization
- [ ] Add video transcoding endpoints
- [ ] Implement webhook notifications
- [ ] Add monitoring and logging
- [ ] Write comprehensive tests
