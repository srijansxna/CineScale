# PostgreSQL Schema Implementation - Complete

## ✅ What Was Created

### 1. SQLAlchemy Models (`services/api/db/schema.py`)

Complete async SQLAlchemy models with:
- **Video** - Core video information and metadata
- **Job** - Processing job tracking with progress
- **VideoVariant** - Multiple resolutions/formats
- **Thumbnail** - Video thumbnail images

**Features:**
- Proper relationships (one-to-many, foreign keys)
- Cascade deletes
- Indexes for performance
- Enums for status fields
- Timestamps with auto-update
- Constraints (progress 0-100, unique constraints)
- Comments and documentation

### 2. Raw SQL Schema (`services/api/db/schema.sql`)

Pure PostgreSQL schema with:
- CREATE TABLE statements
- Enum types
- Indexes
- Foreign keys with CASCADE
- Check constraints
- Comments

### 3. Initialization Script (`services/api/db/init_schema.py`)

Automated schema creation:
- Creates all tables
- Shows summary of tables, columns, indexes
- Can be run multiple times safely

### 4. Documentation

- **DATABASE_SCHEMA.md** - Complete schema documentation
- **SCHEMA_DIAGRAM.md** - Visual diagrams and relationships
- **SCHEMA_IMPLEMENTATION.md** - This file

### 5. Test Script (`test_schema.py`)

Comprehensive test that:
- Creates sample video
- Creates job
- Creates variants (1080p, 720p, 480p)
- Creates thumbnails
- Queries and displays all data

---

## Schema Overview

### Tables

| Table | Purpose | Rows per Video |
|-------|---------|----------------|
| **videos** | Core video info | 1 |
| **jobs** | Processing jobs | 1-5 |
| **video_variants** | Resolutions | 3-5 |
| **thumbnails** | Preview images | 4-10 |

### Relationships

```
videos (1) ──< (N) jobs
  │
  ├──< (N) video_variants
  │
  └──< (N) thumbnails
```

### Key Features

✅ **UUIDs** for external references (video_id, job_id)  
✅ **Enums** for status fields (type-safe)  
✅ **Indexes** on frequently queried fields  
✅ **Foreign keys** with CASCADE delete  
✅ **Timestamps** with auto-update  
✅ **Soft deletes** for videos  
✅ **Progress tracking** (0-100)  
✅ **Retry logic** for jobs  
✅ **Unique constraints** (video_id, resolution pairs)  

---

## Quick Start

### 1. Initialize Schema

```bash
# Using SQLAlchemy (recommended)
python services/api/db/init_schema.py

# Or using raw SQL
psql -U postgres -d cinescale -f services/api/db/schema.sql
```

### 2. Test Schema

```bash
python test_schema.py
```

Expected output:
```
🧪 Testing Database Schema
==================================================

1. Creating video...
   ✅ Created: <Video(id=1, video_id=test-video-001, filename=test.mp4)>

2. Creating job...
   ✅ Created: <Job(id=1, job_id=test-job-001, status=JobStatus.PENDING)>

3. Creating video variants...
   ✅ Created variant: 1080p
   ✅ Created variant: 720p
   ✅ Created variant: 480p

4. Creating thumbnails...
   ✅ Created thumbnail at 0.0s
   ✅ Created thumbnail at 30.0s
   ✅ Created thumbnail at 60.0s
   ✅ Created thumbnail at 90.0s

✅ All data committed successfully!
```

---

## Usage Examples

### Create Video with Job

```python
from services.api.db.schema import Video, Job, VideoStatus, JobStatus
from services.api.db.postgres import async_session_maker

async def create_video():
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

### Query Video with Relationships

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
        video = result.scalar_one_or_none()
        
        if video:
            print(f"Video: {video.filename}")
            print(f"Jobs: {len(video.jobs)}")
            print(f"Variants: {len(video.variants)}")
            print(f"Thumbnails: {len(video.thumbnails)}")
        
        return video
```

### Update Job Progress

```python
async def update_job_progress(job_id: str, progress: int):
    async with async_session_maker() as session:
        result = await session.execute(
            select(Job).where(Job.job_id == job_id)
        )
        job = result.scalar_one_or_none()
        
        if job:
            job.progress = progress
            if progress == 100:
                job.status = JobStatus.DONE
                job.completed_at = func.now()
            else:
                job.status = JobStatus.PROCESSING
            
            await session.commit()
```

### Create Variants

```python
async def create_variants(video_id: str):
    async with async_session_maker() as session:
        resolutions = [
            ("1080p", 1920, 1080),
            ("720p", 1280, 720),
            ("480p", 854, 480),
        ]
        
        for resolution, width, height in resolutions:
            variant = VideoVariant(
                video_id=video_id,
                resolution=resolution,
                width=width,
                height=height,
                url=f"/api/videos/{video_id}/stream/{resolution}",
                status=VariantStatus.PENDING
            )
            session.add(variant)
        
        await session.commit()
```

---

## Schema Files

```
services/api/db/
├── schema.py              # SQLAlchemy models ⭐
├── schema.sql             # Raw SQL schema
├── init_schema.py         # Initialization script
├── postgres.py            # Database connection
└── pg_models.py           # Old models (deprecated)

Documentation:
├── DATABASE_SCHEMA.md     # Complete documentation
├── SCHEMA_DIAGRAM.md      # Visual diagrams
└── SCHEMA_IMPLEMENTATION.md  # This file

Tests:
└── test_schema.py         # Schema test script
```

---

## Comparison: Old vs New Schema

### Old Schema (pg_models.py)
- 2 tables: videos, processing_jobs
- Basic fields only
- No variants or thumbnails
- Limited metadata

### New Schema (schema.py)
- 4 tables: videos, jobs, video_variants, thumbnails
- Complete metadata fields
- Multiple resolutions support
- Thumbnail management
- Better status tracking
- Retry logic
- Soft deletes
- More indexes

---

## Migration Path

### Option 1: Fresh Start (Recommended for Development)

```bash
# Drop old tables
psql -U postgres -d cinescale -c "DROP TABLE IF EXISTS processing_jobs, videos CASCADE;"

# Create new schema
python services/api/db/init_schema.py
```

### Option 2: Gradual Migration

```bash
# Keep old tables
# Create new tables with different names
# Migrate data gradually
# Switch over when ready
```

---

## Performance

### Indexes Created

**videos:**
- video_id (unique)
- status
- (status, created_at)
- upload_time

**jobs:**
- job_id (unique)
- video_id
- status
- (status, created_at)
- (video_id, status)

**video_variants:**
- video_id
- status
- (video_id, resolution) unique

**thumbnails:**
- video_id
- (video_id, timestamp)
- (video_id, is_primary)

### Query Performance

| Query | Index Used | Speed |
|-------|-----------|-------|
| Get video by video_id | video_id (unique) | O(1) |
| Get pending jobs | status | O(log n) |
| Get video variants | video_id | O(log n) |
| Get primary thumbnail | (video_id, is_primary) | O(log n) |

---

## Next Steps

1. ✅ Schema designed and implemented
2. ✅ SQLAlchemy models created
3. ✅ Documentation complete
4. ⏳ Update API endpoints to use new schema
5. ⏳ Implement worker to populate variants
6. ⏳ Add thumbnail generation
7. ⏳ Add video transcoding
8. ⏳ Add database migrations (Alembic)

---

## Summary

Complete PostgreSQL schema for video processing pipeline with:
- 4 tables (videos, jobs, video_variants, thumbnails)
- Proper relationships and foreign keys
- Comprehensive indexes
- Status enums
- Progress tracking
- Retry logic
- Soft deletes
- Full documentation

All files created and ready to use! 🚀
