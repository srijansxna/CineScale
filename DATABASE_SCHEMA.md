# PostgreSQL Schema - Video Processing Pipeline

## Overview

Complete database schema for a video processing pipeline with support for:
- Video uploads and metadata
- Processing job tracking with progress
- Multiple video variants/resolutions
- Thumbnail generation and storage

## Tables

### 1. videos
**Core video information and metadata**

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL | Primary key |
| `video_id` | VARCHAR(36) | UUID, unique identifier |
| `filename` | VARCHAR(255) | Original filename |
| `file_path` | VARCHAR(512) | Storage path |
| `file_size` | BIGINT | File size in bytes |
| `content_type` | VARCHAR(100) | MIME type |
| `duration` | FLOAT | Duration in seconds |
| `width` | INTEGER | Video width in pixels |
| `height` | INTEGER | Video height in pixels |
| `codec` | VARCHAR(50) | Video codec |
| `bitrate` | INTEGER | Bitrate in kbps |
| `fps` | FLOAT | Frames per second |
| `status` | ENUM | UPLOADED, QUEUED, PROCESSING, COMPLETED, FAILED, DELETED |
| `upload_time` | TIMESTAMP | Upload timestamp |
| `created_at` | TIMESTAMP | Creation timestamp |
| `updated_at` | TIMESTAMP | Last update timestamp |
| `deleted_at` | TIMESTAMP | Soft delete timestamp |

**Indexes:**
- `video_id` (unique)
- `status`
- `(status, created_at)` (composite)
- `upload_time`

**Relationships:**
- One-to-many with `jobs`
- One-to-many with `video_variants`
- One-to-many with `thumbnails`

---

### 2. jobs
**Processing job tracking**

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL | Primary key |
| `job_id` | VARCHAR(36) | UUID, unique identifier |
| `video_id` | VARCHAR(36) | Foreign key to videos |
| `job_type` | VARCHAR(50) | Job type: transcode, thumbnail, etc. |
| `status` | ENUM | PENDING, PROCESSING, DONE, FAILED, CANCELLED |
| `progress` | INTEGER | Progress percentage (0-100) |
| `result` | TEXT | JSON result data |
| `error` | TEXT | Error message if failed |
| `worker_id` | VARCHAR(100) | Worker that processed this job |
| `created_at` | TIMESTAMP | Creation timestamp |
| `updated_at` | TIMESTAMP | Last update timestamp |
| `started_at` | TIMESTAMP | When job started processing |
| `completed_at` | TIMESTAMP | When job completed |
| `retry_count` | INTEGER | Number of retry attempts |
| `max_retries` | INTEGER | Maximum retry attempts |

**Indexes:**
- `job_id` (unique)
- `video_id`
- `status`
- `(status, created_at)` (composite)
- `(video_id, status)` (composite)

**Relationships:**
- Many-to-one with `videos`

**Constraints:**
- `progress` CHECK (progress >= 0 AND progress <= 100)
- Foreign key cascade delete

---

### 3. video_variants
**Different video resolutions and formats**

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL | Primary key |
| `video_id` | VARCHAR(36) | Foreign key to videos |
| `resolution` | VARCHAR(20) | 240p, 360p, 480p, 720p, 1080p, 1440p, 4k |
| `width` | INTEGER | Width in pixels |
| `height` | INTEGER | Height in pixels |
| `file_path` | VARCHAR(512) | Storage path for variant |
| `file_size` | BIGINT | File size in bytes |
| `url` | VARCHAR(512) | Streaming URL |
| `codec` | VARCHAR(50) | Video codec |
| `bitrate` | INTEGER | Bitrate in kbps |
| `fps` | FLOAT | Frames per second |
| `status` | ENUM | PENDING, PROCESSING, READY, FAILED |
| `created_at` | TIMESTAMP | Creation timestamp |
| `updated_at` | TIMESTAMP | Last update timestamp |

**Indexes:**
- `video_id`
- `status`
- `(video_id, resolution)` (unique composite)

**Relationships:**
- Many-to-one with `videos`

**Constraints:**
- Unique constraint on `(video_id, resolution)`
- Foreign key cascade delete

---

### 4. thumbnails
**Video thumbnail images**

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL | Primary key |
| `video_id` | VARCHAR(36) | Foreign key to videos |
| `timestamp` | FLOAT | Timestamp in video (seconds) |
| `filename` | VARCHAR(255) | Thumbnail filename |
| `file_path` | VARCHAR(512) | Storage path |
| `file_size` | INTEGER | File size in bytes |
| `url` | VARCHAR(512) | Thumbnail URL |
| `width` | INTEGER | Thumbnail width in pixels |
| `height` | INTEGER | Thumbnail height in pixels |
| `format` | VARCHAR(10) | Image format: jpg, png, webp |
| `is_primary` | BOOLEAN | Primary thumbnail for video |
| `created_at` | TIMESTAMP | Creation timestamp |

**Indexes:**
- `video_id`
- `(video_id, timestamp)` (composite)
- `(video_id, is_primary)` (composite)

**Relationships:**
- Many-to-one with `videos`

**Constraints:**
- Foreign key cascade delete

---

## Entity Relationship Diagram

```
┌─────────────────┐
│     videos      │
│─────────────────│
│ id (PK)         │
│ video_id (UK)   │
│ filename        │
│ file_path       │
│ file_size       │
│ status          │
│ upload_time     │
│ ...             │
└────────┬────────┘
         │
         │ 1:N
         │
    ┌────┴────┬────────────┬──────────┐
    │         │            │          │
    ▼         ▼            ▼          ▼
┌───────┐ ┌──────────┐ ┌─────────┐ ┌────────────┐
│ jobs  │ │ variants │ │ thumbs  │ │  (future)  │
└───────┘ └──────────┘ └─────────┘ └────────────┘
```

---

## Enums

### VideoStatus
- `UPLOADED` - Video uploaded, not yet queued
- `QUEUED` - Queued for processing
- `PROCESSING` - Currently being processed
- `COMPLETED` - Processing completed successfully
- `FAILED` - Processing failed
- `DELETED` - Soft deleted

### JobStatus
- `PENDING` - Job created, waiting to start
- `PROCESSING` - Job is being processed
- `DONE` - Job completed successfully
- `FAILED` - Job failed
- `CANCELLED` - Job was cancelled

### VariantStatus
- `PENDING` - Variant queued for creation
- `PROCESSING` - Variant being created
- `READY` - Variant ready for streaming
- `FAILED` - Variant creation failed

---

## SQLAlchemy Models

### Usage Example

```python
from services.api.db.schema import Video, Job, VideoVariant, Thumbnail
from services.api.db.postgres import async_session_maker

async def create_video_with_job():
    async with async_session_maker() as session:
        # Create video
        video = Video(
            video_id="550e8400-e29b-41d4-a716-446655440000",
            filename="demo.mp4",
            file_path="/storage/raw/demo.mp4",
            file_size=15728640,
            status=VideoStatus.UPLOADED
        )
        session.add(video)
        
        # Create job
        job = Job(
            job_id="6ba7b810-9dad-11d1-80b4-00c04fd430c8",
            video_id=video.video_id,
            status=JobStatus.PENDING,
            progress=0
        )
        session.add(job)
        
        await session.commit()
```

---

## Initialization

### Using SQLAlchemy (Recommended)

```bash
# Initialize schema
python services/api/db/init_schema.py
```

### Using SQL Directly

```bash
# Execute SQL file
psql -U postgres -d cinescale -f services/api/db/schema.sql
```

---

## Queries

### Get video with all related data

```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def get_video_complete(video_id: str):
    async with async_session_maker() as session:
        result = await session.execute(
            select(Video)
            .options(
                selectinload(Video.jobs),
                selectinload(Video.variants),
                selectinload(Video.thumbnails)
            )
            .where(Video.video_id == video_id)
        )
        return result.scalar_one_or_none()
```

### Get pending jobs

```python
async def get_pending_jobs():
    async with async_session_maker() as session:
        result = await session.execute(
            select(Job)
            .where(Job.status == JobStatus.PENDING)
            .order_by(Job.created_at)
        )
        return result.scalars().all()
```

### Get ready variants for video

```python
async def get_ready_variants(video_id: str):
    async with async_session_maker() as session:
        result = await session.execute(
            select(VideoVariant)
            .where(
                VideoVariant.video_id == video_id,
                VideoVariant.status == VariantStatus.READY
            )
            .order_by(VideoVariant.height.desc())
        )
        return result.scalars().all()
```

---

## Migration

### Add new column

```python
# Migration script
async def add_column():
    async with engine.begin() as conn:
        await conn.execute(text("""
            ALTER TABLE videos 
            ADD COLUMN new_field VARCHAR(100)
        """))
```

### Create index

```python
async def create_index():
    async with engine.begin() as conn:
        await conn.execute(text("""
            CREATE INDEX idx_videos_new_field 
            ON videos(new_field)
        """))
```

---

## Performance Considerations

### Indexes
- All foreign keys are indexed
- Status fields are indexed for filtering
- Composite indexes for common query patterns
- Unique indexes for UUID fields

### Cascade Deletes
- Deleting a video cascades to:
  - All jobs
  - All variants
  - All thumbnails

### Soft Deletes
- Videos have `deleted_at` for soft deletion
- Allows recovery and audit trail

---

## Best Practices

1. **Always use video_id/job_id** (UUIDs) in APIs, not database IDs
2. **Use transactions** for operations affecting multiple tables
3. **Update timestamps** automatically via `onupdate`
4. **Check constraints** ensure data integrity (e.g., progress 0-100)
5. **Use enums** for status fields to prevent invalid values
6. **Index frequently queried fields** (status, timestamps)
7. **Use relationships** for easier querying with SQLAlchemy

---

## Files

- `services/api/db/schema.py` - SQLAlchemy models
- `services/api/db/schema.sql` - Raw SQL schema
- `services/api/db/init_schema.py` - Initialization script
- `DATABASE_SCHEMA.md` - This documentation
