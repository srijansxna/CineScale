# Database Schema Diagram

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                          VIDEOS                             │
├─────────────────────────────────────────────────────────────┤
│ PK  id                    SERIAL                            │
│ UK  video_id              VARCHAR(36)                       │
│     filename              VARCHAR(255)                      │
│     file_path             VARCHAR(512)                      │
│     file_size             BIGINT                            │
│     content_type          VARCHAR(100)                      │
│     duration              FLOAT                             │
│     width                 INTEGER                           │
│     height                INTEGER                           │
│     codec                 VARCHAR(50)                       │
│     bitrate               INTEGER                           │
│     fps                   FLOAT                             │
│     status                ENUM(VideoStatus)                 │
│     upload_time           TIMESTAMP                         │
│     created_at            TIMESTAMP                         │
│     updated_at            TIMESTAMP                         │
│     deleted_at            TIMESTAMP                         │
└──────────────┬──────────────────────────────────────────────┘
               │
               │ 1:N
               │
    ┌──────────┼──────────┬──────────────┐
    │          │          │              │
    ▼          ▼          ▼              ▼
┌───────┐  ┌──────┐  ┌────────┐  ┌──────────┐
│ JOBS  │  │VARIA │  │THUMBNA │  │ FUTURE   │
│       │  │NTS   │  │ILS     │  │ TABLES   │
└───────┘  └──────┘  └────────┘  └──────────┘

┌─────────────────────────────────────────────────────────────┐
│                           JOBS                              │
├─────────────────────────────────────────────────────────────┤
│ PK  id                    SERIAL                            │
│ UK  job_id                VARCHAR(36)                       │
│ FK  video_id              VARCHAR(36) → videos.video_id    │
│     job_type              VARCHAR(50)                       │
│     status                ENUM(JobStatus)                   │
│     progress              INTEGER (0-100)                   │
│     result                TEXT (JSON)                       │
│     error                 TEXT                              │
│     worker_id             VARCHAR(100)                      │
│     created_at            TIMESTAMP                         │
│     updated_at            TIMESTAMP                         │
│     started_at            TIMESTAMP                         │
│     completed_at          TIMESTAMP                         │
│     retry_count           INTEGER                           │
│     max_retries           INTEGER                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      VIDEO_VARIANTS                         │
├─────────────────────────────────────────────────────────────┤
│ PK  id                    SERIAL                            │
│ FK  video_id              VARCHAR(36) → videos.video_id    │
│     resolution            VARCHAR(20)                       │
│     width                 INTEGER                           │
│     height                INTEGER                           │
│     file_path             VARCHAR(512)                      │
│     file_size             BIGINT                            │
│     url                   VARCHAR(512)                      │
│     codec                 VARCHAR(50)                       │
│     bitrate               INTEGER                           │
│     fps                   FLOAT                             │
│     status                ENUM(VariantStatus)               │
│     created_at            TIMESTAMP                         │
│     updated_at            TIMESTAMP                         │
│ UK  (video_id, resolution)                                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                        THUMBNAILS                           │
├─────────────────────────────────────────────────────────────┤
│ PK  id                    SERIAL                            │
│ FK  video_id              VARCHAR(36) → videos.video_id    │
│     timestamp             FLOAT                             │
│     filename              VARCHAR(255)                      │
│     file_path             VARCHAR(512)                      │
│     file_size             INTEGER                           │
│     url                   VARCHAR(512)                      │
│     width                 INTEGER                           │
│     height                INTEGER                           │
│     format                VARCHAR(10)                       │
│     is_primary            BOOLEAN                           │
│     created_at            TIMESTAMP                         │
└─────────────────────────────────────────────────────────────┘
```

## Relationships

```
videos (1) ──< (N) jobs
  │
  ├──< (N) video_variants
  │
  └──< (N) thumbnails
```

## Status Flow Diagrams

### Video Status Flow
```
UPLOADED → QUEUED → PROCESSING → COMPLETED
                         ↓
                      FAILED
                         ↓
                      DELETED
```

### Job Status Flow
```
PENDING → PROCESSING → DONE
             ↓
          FAILED ←→ PENDING (retry)
             ↓
         CANCELLED
```

### Variant Status Flow
```
PENDING → PROCESSING → READY
             ↓
          FAILED
```

## Indexes Summary

### videos
- `video_id` (unique)
- `status`
- `(status, created_at)`
- `upload_time`

### jobs
- `job_id` (unique)
- `video_id`
- `status`
- `(status, created_at)`
- `(video_id, status)`

### video_variants
- `video_id`
- `status`
- `(video_id, resolution)` (unique)

### thumbnails
- `video_id`
- `(video_id, timestamp)`
- `(video_id, is_primary)`

## Data Types

| Type | Usage | Example |
|------|-------|---------|
| SERIAL | Auto-increment IDs | 1, 2, 3... |
| VARCHAR(36) | UUIDs | 550e8400-e29b-41d4-a716-446655440000 |
| VARCHAR(255) | Filenames | demo.mp4 |
| VARCHAR(512) | Paths/URLs | /storage/raw/video.mp4 |
| BIGINT | File sizes | 15728640 (bytes) |
| INTEGER | Dimensions, bitrate | 1920, 5000 |
| FLOAT | Duration, FPS | 120.5, 30.0 |
| TEXT | JSON, errors | {"metadata": {...}} |
| BOOLEAN | Flags | true, false |
| TIMESTAMP | Dates/times | 2024-03-12 10:30:00+00 |
| ENUM | Status values | PENDING, DONE |

## Constraints

### Primary Keys
- All tables have `id` as SERIAL primary key

### Unique Constraints
- `videos.video_id`
- `jobs.job_id`
- `(video_variants.video_id, video_variants.resolution)`

### Foreign Keys
- `jobs.video_id` → `videos.video_id` (CASCADE DELETE)
- `video_variants.video_id` → `videos.video_id` (CASCADE DELETE)
- `thumbnails.video_id` → `videos.video_id` (CASCADE DELETE)

### Check Constraints
- `jobs.progress` BETWEEN 0 AND 100

## Storage Estimates

### Per Video (1080p, 2 minutes)

| Item | Size | Count | Total |
|------|------|-------|-------|
| Original video | 50 MB | 1 | 50 MB |
| 1080p variant | 50 MB | 1 | 50 MB |
| 720p variant | 25 MB | 1 | 25 MB |
| 480p variant | 15 MB | 1 | 15 MB |
| Thumbnails | 50 KB | 4 | 200 KB |
| **Total** | | | **~140 MB** |

### Database Row Size

| Table | Avg Size | Per 1000 Videos |
|-------|----------|-----------------|
| videos | ~500 bytes | 500 KB |
| jobs | ~300 bytes | 300 KB |
| video_variants | ~200 bytes | 600 KB (3 variants) |
| thumbnails | ~150 bytes | 600 KB (4 thumbs) |
| **Total** | | **~2 MB** |
