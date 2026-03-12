# GET /api/job/{job_id} - Implementation

## ✅ Endpoint Complete

**URL:** `GET /api/job/{job_id}`  
**Purpose:** Get video processing job status with progress tracking

## Job States

| State | Progress | Description |
|-------|----------|-------------|
| `PENDING` | 0% | Job created, waiting to be processed |
| `PROCESSING` | 1-99% | Job is currently being processed |
| `DONE` | 100% | Job completed successfully |
| `FAILED` | varies | Job failed with error |

## Request

```bash
GET /api/job/{job_id}
```

**Path Parameters:**
- `job_id` (string, required) - Unique job identifier

## Response

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "video_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "status": "PROCESSING",
  "progress": 45,
  "result": null,
  "error": null,
  "created_at": "2024-03-12T10:30:00Z",
  "updated_at": "2024-03-12T10:30:45Z"
}
```

**Response Fields:**
- `job_id` - Unique job identifier
- `video_id` - Associated video identifier
- `status` - Current job state (PENDING/PROCESSING/DONE/FAILED)
- `progress` - Progress percentage (0-100)
- `result` - Processing results (available when DONE)
- `error` - Error message (available when FAILED)
- `created_at` - Job creation timestamp
- `updated_at` - Last update timestamp

## Examples

### 1. Pending Job
```bash
curl http://localhost:8000/api/job/550e8400-e29b-41d4-a716-446655440000
```

Response:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "video_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "status": "PENDING",
  "progress": 0,
  "result": null,
  "error": null,
  "created_at": "2024-03-12T10:30:00Z",
  "updated_at": null
}
```

### 2. Processing Job
```json
{
  "status": "PROCESSING",
  "progress": 65,
  "updated_at": "2024-03-12T10:31:30Z"
}
```

### 3. Completed Job
```json
{
  "status": "DONE",
  "progress": 100,
  "result": {
    "metadata": {
      "duration": 120.5,
      "width": 1920,
      "height": 1080
    },
    "thumbnails": ["thumb1.jpg", "thumb2.jpg"]
  }
}
```

### 4. Failed Job
```json
{
  "status": "FAILED",
  "progress": 30,
  "error": "Video codec not supported"
}
```

### 5. Job Not Found
```bash
curl http://localhost:8000/api/job/invalid-id
```

Response (404):
```json
{
  "detail": "Job invalid-id not found"
}
```

## Testing

### Automated Test
```bash
chmod +x test_job_status.sh
./test_job_status.sh
```

### Manual Test
```bash
# 1. Upload a video
RESPONSE=$(curl -s -X POST http://localhost:8000/api/upload \
  -F "file=@video.mp4")

# 2. Extract job_id
JOB_ID=$(echo $RESPONSE | jq -r '.job_id')

# 3. Check status
curl http://localhost:8000/api/job/$JOB_ID | jq
```

### Interactive Docs
Visit: http://localhost:8000/docs

## Database Schema

**processing_jobs table:**
```sql
CREATE TABLE processing_jobs (
    id SERIAL PRIMARY KEY,
    job_id VARCHAR UNIQUE NOT NULL,
    video_id VARCHAR NOT NULL,
    status VARCHAR NOT NULL,  -- PENDING, PROCESSING, DONE, FAILED
    progress INTEGER DEFAULT 0 NOT NULL,  -- 0-100
    result JSON,
    error VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

## Implementation Files

```
services/api/
├── routes/
│   └── jobs.py                    # GET /api/job/{job_id}
├── schemas/
│   └── job_status.py              # JobStatusResponse model
├── services/
│   └── video_service.py           # get_job_by_id, update_job_status
└── db/
    ├── pg_models.py               # ProcessingJob model with progress
    └── migrate_add_progress.py    # Migration script
```

## Progress Tracking

Progress is automatically set based on status:
- `PENDING` → 0%
- `PROCESSING` → 1-99% (manually updated by worker)
- `DONE` → 100%
- `FAILED` → keeps last progress value

## Worker Integration

Workers can update job progress:

```python
from services.api.services.video_service import VideoService
from services.api.db.models import JobStatus

# Update progress during processing
await video_service.update_job_status(
    job_id="550e8400-...",
    status=JobStatus.PROCESSING,
    progress=50
)

# Mark as complete
await video_service.update_job_status(
    job_id="550e8400-...",
    status=JobStatus.DONE,
    progress=100,
    result={"metadata": {...}, "thumbnails": [...]}
)

# Mark as failed
await video_service.update_job_status(
    job_id="550e8400-...",
    status=JobStatus.FAILED,
    error="Processing error message"
)
```

## Features

✅ Job status retrieval  
✅ Progress percentage (0-100)  
✅ Four job states (PENDING/PROCESSING/DONE/FAILED)  
✅ Result data for completed jobs  
✅ Error messages for failed jobs  
✅ Timestamps (created_at, updated_at)  
✅ 404 error for non-existent jobs  
✅ PostgreSQL backed  
✅ Async implementation  

## Next Steps

1. ✅ Job status endpoint
2. Implement worker to update job progress
3. Add webhook notifications
4. Add job listing endpoint
5. Add job cancellation
6. Add job retry logic
