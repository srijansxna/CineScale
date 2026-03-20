# CineScale — Distributed Video Processing Pipeline

## Overview

CineScale is an asynchronous, horizontally-scalable video processing system. A client uploads a video once and immediately receives a `job_id`. All heavy work (transcoding, thumbnail generation) happens off the request path inside isolated Celery workers. Clients poll for status; results are served via pre-signed MinIO URLs.

---

## Component Map

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Client (HTTP)                              │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ POST /api/upload
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        FastAPI  (API Service)                       │
│                                                                     │
│  Routes: /api/upload  /api/job/{id}  /api/videos                   │
│  • Validates file type / size                                       │
│  • Writes Video + ProcessingJob rows  ──────────────────────────┐  │
│  • Dispatches Celery task  ─────────────────────────────────┐   │  │
│  • Returns { job_id, video_id, status: PENDING }            │   │  │
└─────────────────────────────────────────────────────────────┼───┼──┘
                                                              │   │
                          ┌───────────────────────────────────┘   │
                          │  send_task()                           │
                          ▼                                        │
┌─────────────────────────────────────┐                           │
│         Redis  (Message Broker)     │                           │
│                                     │                           │
│  DB 0 — Celery task queue (broker)  │                           │
│  DB 1 — Celery result backend       │                           │
│  DB 2 — Live job progress / status  │                           │
└──────────────────┬──────────────────┘                           │
                   │  task consumed                                │
                   ▼                                               │
┌─────────────────────────────────────────────────────────────────┼──┐
│                    Celery Worker  (worker Service)              │  │
│                                                                 │  │
│  process_video task:                                            │  │
│    1. extract_metadata()   → ffprobe                           │  │
│    2. transcode_video()    → FFmpeg  (360p / 720p / 1080p)     │  │
│    3. generate_thumbnails()→ FFmpeg  (10% / 50% / 90%)         │  │
│    4. StorageService       → upload variants + thumbs to MinIO │  │
│    5. set_status() / update_progress() → Redis DB 2            │  │
│                                                                 │  │
│  Retry policy: max 3 retries, exponential backoff (1s/2s/4s)   │  │
└─────────────────────────────────────────────────────────────────┘  │
                                                                      │
┌─────────────────────────────────────────────────────────────────────┘
│                     PostgreSQL  (Metadata Store)
│
│  Table: videos
│    video_id, filename, file_path, file_size, content_type, created_at
│
│  Table: processing_jobs
│    job_id, video_id, status, progress (0-100), result (JSON), error
└──────────────────────────────────────────────────────────────────────

┌──────────────────────────────────────────────────────────────────────┐
│                        MinIO  (Object Storage)                       │
│                                                                      │
│  Bucket: raw-videos       → original upload                         │
│  Bucket: video-variants   → {video_id}/{resolution}/{file}          │
│  Bucket: thumbnails       → {video_id}/{thumb_name}.jpg             │
│                                                                      │
│  Access: pre-signed URLs (default TTL 3600 s)                       │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Request Flow — Step by Step

### 1. Upload

```
Client  ──POST /api/upload (multipart)──►  FastAPI
```

- FastAPI validates the file extension (`.mp4 .mov .mkv …`) and size (≤ 500 MB).
- `VideoService.create_video_and_job()` streams the file to local disk in 1 MB chunks, then writes two rows to PostgreSQL in a single transaction:
  - `videos` — stores filename, path, size, content type
  - `processing_jobs` — status = `PENDING`, progress = 0
- The transaction is committed before any task is dispatched (worker can't start on a row that doesn't exist yet).

### 2. Queue

```
FastAPI  ──send_task("process_video", task_id=job_id)──►  Redis DB 0
```

- `celery_client.py` calls `send_task()` using the broker URL from settings.
- The Celery task ID is set to `job_id` so result lookups by job ID work without a separate mapping.
- FastAPI returns `{ job_id, video_id, status: "PENDING" }` immediately — the client doesn't wait for processing.

### 3. Worker picks up the task

```
Redis DB 0  ──task message──►  Celery Worker
```

- A worker process (one of N replicas) dequeues the message.
- It sets status = `PROCESSING` in Redis DB 2 and begins the pipeline.

### 4. FFmpeg processing pipeline

```
Worker  ──ffprobe──►  metadata
Worker  ──ffmpeg──►   360p.mp4 / 720p.mp4 / 1080p.mp4
Worker  ──ffmpeg──►   thumb_10pct.jpg / thumb_50pct.jpg / thumb_90pct.jpg
```

Progress is written to Redis DB 2 at each stage:

| Step               | Progress |
|--------------------|----------|
| Initializing       | 0 %      |
| Extracting metadata| 10 %     |
| Transcoding        | 25 %     |
| Generating thumbs  | 80 %     |
| Finalizing         | 95 %     |
| Complete           | 100 %    |

### 5. Storage upload

```
Worker  ──boto3 upload──►  MinIO
                            raw-videos/{video_id}/original.mp4
                            video-variants/{video_id}/360p/video.mp4
                            video-variants/{video_id}/720p/video.mp4
                            video-variants/{video_id}/1080p/video.mp4
                            thumbnails/{video_id}/thumb_10pct.jpg
                            thumbnails/{video_id}/thumb_50pct.jpg
                            thumbnails/{video_id}/thumb_90pct.jpg
```

`StorageService` auto-creates buckets on first run. All objects are accessed via pre-signed URLs generated at query time.

### 6. Job completion

```
Worker  ──set_status("COMPLETED", result={...})──►  Redis DB 2
Worker  ──UPDATE processing_jobs SET status=DONE──►  PostgreSQL
```

The result payload stored in PostgreSQL includes metadata, transcoded file paths, and thumbnail paths.

### 7. Client polls for status

```
Client  ──GET /api/job/{job_id}──►  FastAPI  ──SELECT──►  PostgreSQL
                                                           (status, progress, result)
```

- `GET /api/job/{job_id}` reads from PostgreSQL (source of truth for durable state).
- Live progress during processing is available from Redis DB 2 for low-latency polling.
- On `DONE`, the response includes pre-signed MinIO URLs for all variants and thumbnails.

### 8. Error handling & retries

If the worker throws at any step:
- Status is set to `FAILED` in Redis with the error message.
- Celery retries up to 3 times with exponential backoff (1 s → 2 s → 4 s).
- After max retries, the job is marked permanently `FAILED` in both Redis and PostgreSQL.

---

## Data Stores — Responsibility Split

| Store      | What lives there                                      | Why                                      |
|------------|-------------------------------------------------------|------------------------------------------|
| PostgreSQL | Video metadata, job records, final results            | Durable, queryable, relational           |
| Redis DB 0 | Celery task queue (broker)                            | Fast pub/sub, Celery native              |
| Redis DB 1 | Celery result backend                                 | Task ACK / result retrieval              |
| Redis DB 2 | Live progress updates (progress %, current step)      | Low-latency writes during processing     |
| MinIO      | Raw uploads, transcoded variants, thumbnails          | Scalable object storage, S3-compatible   |

---

## Container Layout (Docker)

```
docker-compose
├── api          — FastAPI  (uvicorn, port 8000)
├── worker       — Celery worker  (concurrency = CPU count)
├── postgres     — PostgreSQL 15
├── redis        — Redis 7
└── minio        — MinIO  (API :9000, Console :9001)
```

Each service is independently buildable from `Services/api/Dockerfile` and `Services/worker/` respectively. Shared environment variables are injected via `.env`.

---

## Kubernetes Deployment

```
Namespace: cinescale
│
├── Deployment: api          (replicas: 2–10, HPA on CPU/RPS)
│     └── Service: api-svc   (ClusterIP → Ingress)
│
├── Deployment: worker       (replicas: 2–20, HPA on Redis queue depth)
│     └── No Service needed  (outbound only)
│
├── StatefulSet: postgres    (replicas: 1, PVC for data volume)
│
├── StatefulSet: redis       (replicas: 1, PVC for AOF persistence)
│
├── StatefulSet: minio       (replicas: 1–4, PVC per node)
│
├── Ingress: cinescale-ingress
│     /api/*  →  api-svc:8000
│
├── ConfigMap: cinescale-config   (non-secret env vars)
└── Secret:    cinescale-secrets  (DB password, MinIO keys, Redis auth)
```

### Scaling strategy

- API pods scale on request rate — stateless, safe to scale freely.
- Worker pods scale on Redis queue depth (KEDA `RedisListLengthScaler` on the Celery queue key). Each worker is CPU-bound due to FFmpeg; set `requests.cpu` accordingly.
- MinIO scales horizontally in distributed mode (4+ nodes) for production; single-node is fine for staging.
- PostgreSQL uses a single primary with read replicas for status queries if needed.

---

## Key Design Decisions

- job_id = Celery task_id — eliminates a lookup table; `AsyncResult(job_id)` works directly.
- DB commit before task dispatch — prevents the worker from starting before the row exists.
- Redis DB 2 for live progress — keeps hot write traffic off PostgreSQL during processing.
- Pre-signed URLs — MinIO buckets stay private; URLs are generated per-request with a TTL, no public ACLs needed.
- Exponential backoff retries — transient FFmpeg or I/O failures recover automatically without manual intervention.
