# CineScale API - All Endpoints

## ✅ Implemented Endpoints

### 1. POST /api/upload
**Upload video file**

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@video.mp4"
```

Response:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "video_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "filename": "demo.mp4",
  "file_size": 1570024,
  "status": "PENDING",
  "created_at": "2024-03-12T10:30:00Z"
}
```

---

### 2. GET /api/job/{job_id}
**Get job status with progress**

```bash
curl http://localhost:8000/api/job/550e8400-e29b-41d4-a716-446655440000
```

Response:
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

---

### 3. GET /api/videos/{video_id}
**Get complete video information**

```bash
curl http://localhost:8000/api/videos/6ba7b810-9dad-11d1-80b4-00c04fd430c8
```

Response:
```json
{
  "video_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "filename": "demo.mp4",
  "file_size": 15728640,
  "content_type": "video/mp4",
  "metadata": {
    "duration": 120.5,
    "width": 1920,
    "height": 1080,
    "codec": "h264",
    "bitrate": 5000,
    "fps": 30.0
  },
  "variants": [
    {
      "resolution": "1080p",
      "width": 1920,
      "height": 1080,
      "file_size": 15728640,
      "url": "/api/videos/6ba7b810/stream/1080p",
      "status": "ready"
    }
  ],
  "thumbnails": [
    "/api/videos/6ba7b810/thumbnails/thumb_1.jpg"
  ],
  "processing": {
    "status": "DONE",
    "progress": 100,
    "job_id": "550e8400-e29b-41d4-a716-446655440000",
    "started_at": "2024-03-12T10:30:00Z",
    "completed_at": "2024-03-12T10:32:00Z",
    "error": null
  },
  "created_at": "2024-03-12T10:30:00Z",
  "updated_at": "2024-03-12T10:32:00Z"
}
```

---

### 4. GET /api/videos/{video_id}/stream/{resolution}
**Stream video at specific resolution**

```bash
curl http://localhost:8000/api/videos/6ba7b810/stream/720p
```

Returns video file (video/mp4)

---

### 5. GET /api/videos/{video_id}/thumbnails/{thumbnail_name}
**Get video thumbnail**

```bash
curl http://localhost:8000/api/videos/6ba7b810/thumbnails/thumb_1.jpg
```

Returns image file (image/jpeg)

---

## Complete Workflow

```bash
# 1. Upload video
UPLOAD=$(curl -s -X POST http://localhost:8000/api/upload \
  -F "file=@video.mp4")

VIDEO_ID=$(echo $UPLOAD | jq -r '.video_id')
JOB_ID=$(echo $UPLOAD | jq -r '.job_id')

# 2. Check job status
curl http://localhost:8000/api/job/$JOB_ID | jq

# 3. Get video details
curl http://localhost:8000/api/videos/$VIDEO_ID | jq

# 4. Stream video (when ready)
curl http://localhost:8000/api/videos/$VIDEO_ID/stream/720p -o output.mp4
```

---

## Quick Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/upload` | POST | Upload video file |
| `/api/job/{job_id}` | GET | Get job status & progress |
| `/api/videos/{video_id}` | GET | Get video details |
| `/api/videos/{video_id}/stream/{resolution}` | GET | Stream video |
| `/api/videos/{video_id}/thumbnails/{name}` | GET | Get thumbnail |
| `/health` | GET | Health check |

---

## Test Scripts

```bash
# Test upload
./test_upload.sh

# Test job status
./test_job_status.sh

# Test video details
./test_video_detail.sh
```

---

## Interactive Documentation

Visit: **http://localhost:8000/docs**

Features:
- Try all endpoints
- See request/response schemas
- Test with sample data
- View examples

---

## Architecture

```
┌─────────┐
│ Client  │
└────┬────┘
     │
     ▼
┌─────────────────┐
│   FastAPI       │
│   (Port 8000)   │
└────┬────────────┘
     │
     ├──► PostgreSQL (Videos, Jobs)
     ├──► Redis (Queue)
     └──► Storage (Files)
```

---

## Database Schema

### videos
- video_id (UUID, PK)
- filename
- file_path
- file_size
- content_type
- created_at
- updated_at

### processing_jobs
- job_id (UUID, PK)
- video_id (FK)
- status (PENDING/PROCESSING/DONE/FAILED)
- progress (0-100)
- result (JSON: metadata, variants, thumbnails)
- error
- created_at
- updated_at

---

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 404 | Not found |
| 400 | Bad request (invalid file) |
| 413 | File too large |
| 500 | Server error |

---

## Features

✅ Video upload with validation  
✅ Job status tracking  
✅ Progress percentage  
✅ Video metadata  
✅ Multiple resolutions/variants  
✅ Thumbnail support  
✅ Video streaming  
✅ PostgreSQL backed  
✅ Async implementation  
✅ Auto-generated docs  

---

## Running

```bash
# Start all services
docker compose -f docker-compose.postgres.yml up

# Access API
open http://localhost:8000/docs
```

---

## Documentation Files

- `UPLOAD_ENDPOINT.md` - Upload endpoint details
- `JOB_STATUS_ENDPOINT.md` - Job status endpoint details
- `VIDEO_DETAIL_ENDPOINT.md` - Video detail endpoint details
- `POSTGRES_SETUP.md` - Database setup
- `QUICKSTART_POSTGRES.md` - Quick start guide
- `IMPLEMENTATION_SUMMARY.md` - Implementation overview

---

## Next Steps

1. ✅ Upload endpoint
2. ✅ Job status endpoint
3. ✅ Video detail endpoint
4. ⏳ Worker for video processing
5. ⏳ Thumbnail generation
6. ⏳ Video transcoding
7. ⏳ Webhook notifications
8. ⏳ Video listing/search

All core endpoints complete! 🚀
