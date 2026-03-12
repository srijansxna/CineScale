# CineScale - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Option 1: Docker (Recommended)

```bash
# 1. Start all services
docker-compose up --build

# 2. Access the API
open http://localhost:8000/docs
```

That's it! Redis, API, and Worker are all running.

### Option 2: Local Development

```bash
# 1. Run setup script
bash scripts/setup.sh

# 2. Start Redis
docker run -d -p 6379:6379 redis:7-alpine

# 3. Run the API
python run.py
```

## 📋 Project Structure

```
services/api/
├── main.py              # FastAPI app entry point
├── config.py            # Environment configuration
├── routes/              # API endpoints
│   ├── upload.py        # POST /api/upload
│   ├── jobs.py          # GET /api/jobs/{id}
│   └── videos.py        # GET /api/videos/{id}
├── db/                  # Database connections
│   ├── database.py      # Redis client
│   └── models.py        # Data models
├── schemas/             # Pydantic schemas
│   ├── video.py         # Video schemas
│   └── job.py           # Job schemas
└── services/            # Business logic
    ├── storage.py       # File operations
    └── job_service.py   # Job management
```

## 🔌 API Endpoints

### Upload Video
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@video.mp4"
```

Response:
```json
{
  "job_id": "abc-123",
  "status": "PENDING",
  "filename": "video.mp4"
}
```

### Check Job Status
```bash
curl http://localhost:8000/api/jobs/abc-123
```

Response:
```json
{
  "job_id": "abc-123",
  "status": "DONE",
  "result": {
    "metadata": {...},
    "thumbnails": [...]
  }
}
```

### Get Video Info
```bash
curl http://localhost:8000/api/videos/abc-123
```

### Stream Video
```bash
curl http://localhost:8000/api/videos/abc-123/stream/720p
```

## 🛠️ Configuration

Create `.env` file:
```env
APP_NAME=CineScale
DEBUG=True
REDIS_HOST=localhost
REDIS_PORT=6379
```

## 📚 Interactive API Docs

Visit: http://localhost:8000/docs

- Try all endpoints
- See request/response schemas
- Test with sample data

## 🧪 Testing

```bash
# Upload a test video
curl -X POST http://localhost:8000/api/upload \
  -F "file=@Services/worker/samples/demo.mp4"

# Check health
curl http://localhost:8000/health
```

## 🐳 Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down

# Rebuild
docker-compose up --build
```

## 📦 What's Included

- ✅ FastAPI with async endpoints
- ✅ Redis for job queue
- ✅ Celery workers
- ✅ Docker & Docker Compose
- ✅ Environment configuration
- ✅ Pydantic validation
- ✅ Service layer pattern
- ✅ Auto-generated API docs

## 🔍 Troubleshooting

### Port already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Redis connection error
```bash
# Check Redis is running
docker ps | grep redis

# Start Redis
docker run -d -p 6379:6379 redis:7-alpine
```

### Import errors
```bash
# Ensure you're in project root
pwd  # Should show /path/to/CineScale-1

# Install dependencies
pip install -r requirements.txt
```

## 📖 Next Steps

1. Read [README_NEW.md](README_NEW.md) for detailed documentation
2. Check [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for changes
3. Explore the code in `services/api/`
4. Customize configuration in `.env`
5. Add your own endpoints in `routes/`

## 💡 Tips

- Use `make dev` for quick local development
- Use `make docker-up` for Docker deployment
- Check logs with `docker-compose logs -f`
- API docs at `/docs` and `/redoc`

## 🆘 Need Help?

- Check the logs: `docker-compose logs -f api`
- Verify Redis: `redis-cli ping`
- Test health: `curl http://localhost:8000/health`
