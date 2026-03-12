# Database Schema - Quick Reference

## Tables at a Glance

| Table | Primary Key | Unique Key | Foreign Key | Purpose |
|-------|-------------|------------|-------------|---------|
| **videos** | id | video_id | - | Core video info |
| **jobs** | id | job_id | video_id | Processing jobs |
| **video_variants** | id | (video_id, resolution) | video_id | Resolutions |
| **thumbnails** | id | - | video_id | Preview images |

## Status Enums

```python
# VideoStatus
UPLOADED → QUEUED → PROCESSING → COMPLETED
                         ↓
                      FAILED → DELETED

# JobStatus  
PENDING → PROCESSING → DONE
             ↓
          FAILED → CANCELLED

# VariantStatus
PENDING → PROCESSING → READY
             ↓
          FAILED
```

## Common Queries

### Get Video with All Data
```python
from sqlalchemy.orm import selectinload

video = await session.execute(
    select(Video)
    .options(
        selectinload(Video.jobs),
        selectinload(Video.variants),
        selectinload(Video.thumbnails)
    )
    .where(Video.video_id == video_id)
)
```

### Get Pending Jobs
```python
jobs = await session.execute(
    select(Job)
    .where(Job.status == JobStatus.PENDING)
    .order_by(Job.created_at)
)
```

### Get Ready Variants
```python
variants = await session.execute(
    select(VideoVariant)
    .where(
        VideoVariant.video_id == video_id,
        VideoVariant.status == VariantStatus.READY
    )
)
```

### Get Primary Thumbnail
```python
thumbnail = await session.execute(
    select(Thumbnail)
    .where(
        Thumbnail.video_id == video_id,
        Thumbnail.is_primary == True
    )
)
```

## Quick Commands

```bash
# Initialize schema
python services/api/db/init_schema.py

# Test schema
python test_schema.py

# Connect to database
psql -U postgres -d cinescale

# View tables
\dt

# Describe table
\d videos

# Count rows
SELECT COUNT(*) FROM videos;

# View recent videos
SELECT video_id, filename, status, created_at 
FROM videos 
ORDER BY created_at DESC 
LIMIT 10;
```

## Model Import

```python
from services.api.db.schema import (
    Video, Job, VideoVariant, Thumbnail,
    VideoStatus, JobStatus, VariantStatus
)
from services.api.db.postgres import async_session_maker
```

## Files

| File | Purpose |
|------|---------|
| `schema.py` | SQLAlchemy models |
| `schema.sql` | Raw SQL |
| `init_schema.py` | Initialize DB |
| `test_schema.py` | Test script |
| `DATABASE_SCHEMA.md` | Full docs |
| `SCHEMA_DIAGRAM.md` | Diagrams |

## Key Fields

### videos
- `video_id` (UUID) - External reference
- `filename` - Original name
- `file_size` - Bytes
- `duration` - Seconds
- `width`, `height` - Pixels
- `status` - VideoStatus enum

### jobs
- `job_id` (UUID) - External reference
- `video_id` - FK to videos
- `status` - JobStatus enum
- `progress` - 0-100
- `result` - JSON text
- `error` - Error message

### video_variants
- `video_id` - FK to videos
- `resolution` - 720p, 1080p, etc.
- `width`, `height` - Pixels
- `url` - Streaming URL
- `status` - VariantStatus enum

### thumbnails
- `video_id` - FK to videos
- `timestamp` - Seconds in video
- `url` - Image URL
- `is_primary` - Boolean

## Relationships

```
Video.jobs → List[Job]
Video.variants → List[VideoVariant]
Video.thumbnails → List[Thumbnail]

Job.video → Video
VideoVariant.video → Video
Thumbnail.video → Video
```
