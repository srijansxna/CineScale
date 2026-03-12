# POST /api/upload - Implementation Summary

## ✅ Requirements Completed

- ✅ Accept video file upload
- ✅ Save file locally
- ✅ Generate video_id (UUID)
- ✅ Create a processing job entry in PostgreSQL
- ✅ Return job_id and video_id
- ✅ Use SQLAlchemy async models

## Implementation

### Endpoint
**URL:** `POST /api/upload`  
**File:** `services/api/routes/upload.py`

### Database Models
**File:** `services/api/db/pg_models.py`

```python
class Video(Base):
    video_id = Column(String, unique=True, index=True)
    filename = Column(String)
    file_path = Column(String)
    file_size = Column(Integer)
    content_type = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class ProcessingJob(Base):
    job_id = Column(String, unique=True, index=True)
    video_id = Column(String, index=True)
    status = Column(Enum: PENDING, PROCESSING, DONE, FAILED)
    result = Column(JSON)
    error = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
```

### Service Layer
**File:** `services/api/services/video_service.py`

```python
class VideoService:
    async def create_video_and_job(file: UploadFile) -> Tuple[Video, ProcessingJob]:
        # 1. Generate video_id and job_id (UUIDs)
        # 2. Save file to storage/raw/{video_id}.ext
        # 3. Create Video record in PostgreSQL
        # 4. Create ProcessingJob record in PostgreSQL
        # 5. Return both records
```

## Usage

### 1. Start Services

**Docker (includes PostgreSQL):**
```bash
docker compose -f docker-compose.postgres.yml up --build
```

**Local:**
```bash
# Start PostgreSQL
brew services start postgresql@15

# Create database
psql postgres -c "CREATE DATABASE cinescale;"

# Initialize tables
python services/api/db/init_db.py

# Start API
python run.py
```

### 2. Upload Video

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@video.mp4"
```

### 3. Response

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "video_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "filename": "video.mp4",
  "file_size": 15728640,
  "status": "PENDING",
  "created_at": "2024-03-12T10:30:00Z"
}
```

## File Structure

```
services/api/
├── routes/
│   └── upload.py              # POST /api/upload endpoint
├── db/
│   ├── postgres.py            # Async engine & session
│   ├── pg_models.py           # SQLAlchemy models
│   └── init_db.py             # Database initialization
├── services/
│   └── video_service.py       # Business logic
└── schemas/
    └── upload.py              # Pydantic response schema
```

## Testing

### Automated Test
```bash
./test_upload.sh
```

### Manual Test
```bash
# 1. Health check
curl http://localhost:8000/health

# 2. Upload
curl -X POST http://localhost:8000/api/upload \
  -F "file=@Services/worker/samples/demo.mp4" | jq

# 3. Verify in database
psql cinescale -c "SELECT * FROM videos;"
psql cinescale -c "SELECT * FROM processing_jobs;"
```

### Interactive API Docs
Visit: http://localhost:8000/docs

## Dependencies Added

```txt
sqlalchemy[asyncio]==2.0.25
asyncpg==0.29.0
alembic==1.13.1
```

Install:
```bash
pip install -r requirements.txt
```

## Configuration

**.env**
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/cinescale
STORAGE_RAW_DIR=storage/raw
MAX_UPLOAD_SIZE=524288000
```

## Features

- **Async/Await**: Full async implementation
- **Validation**: File type and size validation
- **UUID Generation**: Unique IDs for video and job
- **Chunked Upload**: Handles large files efficiently
- **Transaction Safety**: Database commits/rollbacks
- **Error Handling**: Proper HTTP status codes
- **Type Safety**: Pydantic schemas
- **Auto Documentation**: OpenAPI/Swagger docs

## Next Steps

1. Update job status endpoint to use PostgreSQL
2. Add video listing endpoint
3. Implement job result updates from worker
4. Add database migrations
5. Add video metadata extraction
