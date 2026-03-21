# CineScale

A distributed video processing platform — upload a video, get back multiple resolutions, thumbnails, and metadata. Inspired by how Netflix and YouTube handle video ingestion at scale.

## What it does

1. Upload a video via the React frontend
2. FastAPI saves the file and dispatches a Celery job
3. The worker transcodes to 360p / 720p / 1080p using FFmpeg
4. Thumbnails are extracted at 10%, 50%, 90% of the video duration
5. Job progress is tracked in PostgreSQL and polled live by the frontend
6. Watch the finished video in any resolution directly in the browser

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite + TypeScript + Tailwind CSS + Framer Motion |
| API | FastAPI (Python 3.11) |
| Task queue | Celery + Redis |
| Database | PostgreSQL (async via SQLAlchemy + asyncpg) |
| Video processing | FFmpeg |
| Storage | Local filesystem (MinIO-ready) |
| Containerisation | Docker + Docker Compose |

---

## Project Structure

```
CineScale/
├── Services/
│   ├── api/                  # FastAPI application
│   │   ├── routes/           # upload, jobs, videos endpoints
│   │   ├── services/         # VideoService, StorageService
│   │   ├── db/               # SQLAlchemy models + Postgres setup
│   │   ├── schemas/          # Pydantic request/response models
│   │   ├── config.py         # Settings (pydantic-settings)
│   │   └── Dockerfile
│   ├── worker/               # Celery worker
│   │   ├── tasks.py          # process_video task
│   │   ├── celery_app.py     # Celery app config
│   │   └── job_status.py     # Redis status helpers
│   └── transcoder/           # FFmpeg wrappers
│       ├── transcode.py      # Multi-resolution transcoding
│       ├── thumbnails.py     # Thumbnail extraction
│       └── metadata.py       # Video metadata extraction
├── mini-netflix-frontend/    # React frontend
│   └── src/
│       ├── pages/            # Dashboard, Upload, JobStatus, VideoDetail
│       ├── components/       # VideoCard, UploadBox, Navbar, skeletons…
│       ├── hooks/            # useUpload, useJobStatus
│       ├── services/         # Axios API client
│       └── lib/              # React Query, motion variants
├── storage/                  # Mounted volume for raw + output files
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

---

## Running locally

**Prerequisites:** Docker Desktop running, Node.js 18+

### 1 — Backend (Terminal 1)

```bash
docker compose up
```

First run takes ~10 minutes (FFmpeg install). Subsequent starts take ~5 seconds.

### 2 — Frontend (Terminal 2)

```bash
cd mini-netflix-frontend
npm install
npm run dev
```

Open **http://localhost:5173**

### Ports

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| API + Swagger | http://localhost:8000/docs |
| MinIO console | http://localhost:9001 (minioadmin / minioadmin) |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |

---

## Stopping

```bash
# Stop frontend: Ctrl+C in terminal 2

# Stop backend
docker compose down

# Stop and wipe all data (videos, DB, Redis)
docker compose down -v
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/upload` | Upload a video file |
| GET | `/api/job/{job_id}` | Poll job status + progress |
| GET | `/api/videos` | List all videos |
| GET | `/api/videos/{video_id}` | Video detail + metadata + variants |
| GET | `/api/videos/{video_id}/stream/{resolution}` | Stream a resolution (360p/720p/1080p) |
| GET | `/api/videos/{video_id}/thumbnails/{name}` | Fetch a thumbnail |

---

## Environment variables

Copy `.env.example` to `.env` before running outside Docker:

```bash
cp .env.example .env
```

Key variables:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/cinescale
REDIS_HOST=localhost
CELERY_BROKER_URL=redis://localhost:6379/0
MINIO_ENDPOINT=http://localhost:9000
```

---

## Processing pipeline

```
Upload → Save to disk → Create DB record → Dispatch Celery task
                                                    ↓
                                          Extract metadata (ffprobe)
                                                    ↓
                                     Transcode → 360p / 720p / 1080p
                                                    ↓
                                   Generate thumbnails at 10% / 50% / 90%
                                                    ↓
                                        Write result to PostgreSQL
                                                    ↓
                                         Frontend polls → DONE ✓
```
