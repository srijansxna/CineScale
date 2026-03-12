# PostgreSQL Setup Guide

## Overview

The `/upload` endpoint now uses PostgreSQL with SQLAlchemy async models for persistent storage.

## Database Schema

### Tables

**videos**
- `id` - Primary key
- `video_id` - Unique video identifier (UUID)
- `filename` - Original filename
- `file_path` - Local storage path
- `file_size` - File size in bytes
- `content_type` - MIME type
- `created_at` - Timestamp
- `updated_at` - Timestamp

**processing_jobs**
- `id` - Primary key
- `job_id` - Unique job identifier (UUID)
- `video_id` - Foreign reference to video
- `status` - PENDING, PROCESSING, DONE, FAILED
- `result` - JSON result data
- `error` - Error message if failed
- `created_at` - Timestamp
- `updated_at` - Timestamp

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Start PostgreSQL, Redis, and API
docker compose -f docker-compose.postgres.yml up --build
```

This automatically:
- Starts PostgreSQL on port 5432
- Starts Redis on port 6379
- Creates database tables
- Starts API on port 8000

### Option 2: Local PostgreSQL

#### 1. Install PostgreSQL

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu/Debian:**
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

#### 2. Create Database

```bash
# Connect to PostgreSQL
psql postgres

# Create database and user
CREATE DATABASE cinescale;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE cinescale TO postgres;
\q
```

#### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/cinescale
```

#### 5. Initialize Database

```bash
python services/api/db/init_db.py
```

#### 6. Start API

```bash
python run.py
```

## API Endpoint

### POST /api/upload

Upload a video file and create processing job.

**Request:**
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@video.mp4"
```

**Response:**
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

**Features:**
- ✅ Validates video file type
- ✅ Checks file size (max 500MB)
- ✅ Generates unique video_id (UUID)
- ✅ Generates unique job_id (UUID)
- ✅ Saves file to local storage
- ✅ Creates Video record in PostgreSQL
- ✅ Creates ProcessingJob record in PostgreSQL
- ✅ Returns job and video information

## Testing

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Upload Video
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@Services/worker/samples/demo.mp4" \
  | jq
```

### 3. Check Database
```bash
# Connect to PostgreSQL
psql postgresql://postgres:postgres@localhost:5432/cinescale

# Query videos
SELECT video_id, filename, file_size, created_at FROM videos;

# Query jobs
SELECT job_id, video_id, status, created_at FROM processing_jobs;
```

## Architecture

### Flow

1. **Client** uploads video via POST /api/upload
2. **FastAPI** validates file type and size
3. **VideoService** generates video_id and job_id
4. **Storage** saves file to `storage/raw/{video_id}.mp4`
5. **PostgreSQL** stores Video and ProcessingJob records
6. **Response** returns job_id and video_id to client

### Components

**Models** (`services/api/db/pg_models.py`)
- SQLAlchemy async models
- Video and ProcessingJob tables

**Database** (`services/api/db/postgres.py`)
- Async engine and session
- Connection management
- Dependency injection

**Service** (`services/api/services/video_service.py`)
- Business logic
- File operations
- Database operations

**Route** (`services/api/routes/upload.py`)
- Endpoint handler
- Validation
- Response formatting

## Troubleshooting

### Connection Error
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution:**
- Ensure PostgreSQL is running: `brew services list`
- Check connection string in `.env`
- Verify database exists: `psql -l`

### Table Not Found
```
sqlalchemy.exc.ProgrammingError: relation "videos" does not exist
```

**Solution:**
```bash
python services/api/db/init_db.py
```

### Import Error
```
ModuleNotFoundError: No module named 'asyncpg'
```

**Solution:**
```bash
pip install -r requirements.txt
```

## Migration from Redis

The old Redis-based job storage is still available in:
- `services/api/services/job_service.py` (Redis)
- `services/api/db/database.py` (Redis)

The new PostgreSQL implementation:
- `services/api/services/video_service.py` (PostgreSQL)
- `services/api/db/postgres.py` (PostgreSQL)
- `services/api/db/pg_models.py` (Models)

Both can coexist. The upload endpoint now uses PostgreSQL.

## Next Steps

1. ✅ Upload endpoint with PostgreSQL
2. Update job status endpoint to query PostgreSQL
3. Add video listing endpoint
4. Implement job result updates
5. Add database migrations with Alembic
6. Add indexes for performance
7. Implement soft deletes
8. Add video metadata extraction
