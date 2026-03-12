# Migration Guide - CineScale Refactoring

## Overview

The project has been refactored from a basic structure to a production-ready, modular FastAPI backend.

## What Changed

### Old Structure
```
Services/
├── api/
│   ├── main.py
│   ├── routes/
│   └── core/jobs.py
```

### New Structure
```
services/
├── api/
│   ├── main.py              # Enhanced with middleware, better routing
│   ├── config.py            # NEW: Environment configuration
│   ├── routes/
│   │   ├── upload.py        # Refactored with async, validation
│   │   ├── jobs.py          # Enhanced with service layer
│   │   └── videos.py        # NEW: Video streaming endpoints
│   ├── db/
│   │   ├── database.py      # NEW: Redis connection management
│   │   └── models.py        # NEW: Data models and enums
│   ├── schemas/
│   │   ├── video.py         # NEW: Pydantic schemas
│   │   └── job.py           # NEW: Job schemas
│   └── services/
│       ├── storage.py       # NEW: File storage abstraction
│       └── job_service.py   # NEW: Job management service
```

## Key Improvements

### 1. Configuration Management
- Environment-based configuration using Pydantic
- Centralized settings in `config.py`
- `.env` file support

### 2. Service Layer Pattern
- `StorageService`: File operations
- `JobService`: Job status management
- Dependency injection using FastAPI's `Depends()`

### 3. Async Endpoints
- All endpoints are now async
- Better performance for I/O operations
- Non-blocking file uploads

### 4. Pydantic Schemas
- Request/response validation
- Type safety
- Auto-generated API docs

### 5. Docker Ready
- Multi-service Docker Compose
- Health checks
- Volume management
- Environment configuration

## Migration Steps

### 1. Install New Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Update Imports
Old:
```python
from services.api.core.jobs import jobs
```

New:
```python
from services.api.services.job_service import JobService, get_job_service
```

### 4. Update Worker Integration
The worker now uses environment variables for Redis connection:
```python
REDIS_HOST=redis
REDIS_PORT=6379
```

### 5. Run with Docker
```bash
docker-compose up --build
```

Or locally:
```bash
python run.py
```

## API Changes

### Upload Endpoint
**Old:**
```
POST /upload
```

**New:**
```
POST /api/upload
```

Response now includes proper typing and validation.

### Job Status
**Old:**
```
GET /job/{job_id}
```

**New:**
```
GET /api/jobs/{job_id}
```

Returns structured `JobStatusResponse` with result data.

### New Endpoints

#### Get Video Info
```
GET /api/videos/{job_id}
```

#### Stream Video
```
GET /api/videos/{job_id}/stream/{resolution}
```

## Breaking Changes

1. **Route Prefixes**: All routes now under `/api` prefix
2. **Response Format**: Responses use Pydantic models
3. **Configuration**: Must use environment variables or `.env` file
4. **Redis Connection**: Now managed through `database.py`

## Backward Compatibility

The old `Services/` directory is preserved. You can:
- Keep both structures during transition
- Gradually migrate endpoints
- Run old and new APIs side-by-side (different ports)

## Testing the New API

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Upload Video
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@video.mp4"
```

### 3. Check Job Status
```bash
curl http://localhost:8000/api/jobs/{job_id}
```

### 4. API Documentation
Visit: http://localhost:8000/docs

## Rollback Plan

If needed, revert to old structure:
1. Keep `Services/` directory
2. Update `docker-compose.yml` to use old paths
3. Restore old `main.py` imports

## Next Steps

1. Test all endpoints
2. Update client applications
3. Deploy to staging
4. Monitor logs and metrics
5. Deploy to production

## Support

For issues or questions:
- Check logs: `docker-compose logs -f api`
- Review diagnostics: `make test`
- Consult README_NEW.md
