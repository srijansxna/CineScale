# Quick Start - PostgreSQL Upload Endpoint

## 🚀 Fastest Way (Docker)

```bash
# 1. Start everything (PostgreSQL + Redis + API)
docker compose -f docker-compose.postgres.yml up --build

# 2. Test upload (in another terminal)
curl -X POST http://localhost:8000/api/upload \
  -F "file=@Services/worker/samples/demo.mp4" | jq
```

Done! API is at http://localhost:8000/docs

---

## 🛠️ Local Development

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start PostgreSQL
```bash
# macOS
brew install postgresql@15
brew services start postgresql@15

# Create database
psql postgres -c "CREATE DATABASE cinescale;"
```

### Step 3: Initialize Database
```bash
python services/api/db/init_db.py
```

### Step 4: Configure
```bash
cp .env.example .env
# Edit .env if needed
```

### Step 5: Start API
```bash
python run.py
```

### Step 6: Test
```bash
./test_upload.sh
```

---

## 📋 What Was Implemented

### POST /api/upload

**Request:**
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@video.mp4"
```

**Response:**
```json
{
  "job_id": "uuid-here",
  "video_id": "uuid-here",
  "filename": "video.mp4",
  "file_size": 15728640,
  "status": "PENDING",
  "created_at": "2024-03-12T10:30:00Z"
}
```

**What It Does:**
1. ✅ Accepts video file upload
2. ✅ Validates file type and size
3. ✅ Generates unique video_id (UUID)
4. ✅ Generates unique job_id (UUID)
5. ✅ Saves file to `storage/raw/{video_id}.ext`
6. ✅ Creates Video record in PostgreSQL
7. ✅ Creates ProcessingJob record in PostgreSQL
8. ✅ Returns job_id and video_id

---

## 🗄️ Database Schema

**videos table:**
- video_id (UUID, unique)
- filename
- file_path
- file_size
- content_type
- created_at
- updated_at

**processing_jobs table:**
- job_id (UUID, unique)
- video_id (references videos)
- status (PENDING/PROCESSING/DONE/FAILED)
- result (JSON)
- error
- created_at
- updated_at

---

## 🧪 Testing

### Automated
```bash
./test_upload.sh
```

### Manual
```bash
# Upload
curl -X POST http://localhost:8000/api/upload \
  -F "file=@Services/worker/samples/demo.mp4"

# Check database
psql cinescale -c "SELECT video_id, filename FROM videos;"
psql cinescale -c "SELECT job_id, status FROM processing_jobs;"
```

### Interactive Docs
http://localhost:8000/docs

---

## 📁 Files Created

```
services/api/
├── db/
│   ├── postgres.py          # Async SQLAlchemy setup
│   ├── pg_models.py         # Video & ProcessingJob models
│   └── init_db.py           # Database initialization
├── services/
│   └── video_service.py     # Upload business logic
├── schemas/
│   └── upload.py            # Response schema
└── routes/
    └── upload.py            # POST /api/upload endpoint

docker-compose.postgres.yml  # Docker setup with PostgreSQL
POSTGRES_SETUP.md           # Detailed setup guide
UPLOAD_ENDPOINT.md          # Implementation details
test_upload.sh              # Test script
```

---

## 🔧 Configuration

**.env**
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/cinescale
STORAGE_RAW_DIR=storage/raw
MAX_UPLOAD_SIZE=524288000
```

---

## 🐛 Troubleshooting

### "Connection refused"
```bash
# Check PostgreSQL is running
brew services list | grep postgresql

# Start it
brew services start postgresql@15
```

### "Database does not exist"
```bash
psql postgres -c "CREATE DATABASE cinescale;"
```

### "Table does not exist"
```bash
python services/api/db/init_db.py
```

### "Module not found"
```bash
pip install -r requirements.txt
```

---

## 📚 Documentation

- **Setup Guide**: [POSTGRES_SETUP.md](POSTGRES_SETUP.md)
- **Implementation**: [UPLOAD_ENDPOINT.md](UPLOAD_ENDPOINT.md)
- **API Docs**: http://localhost:8000/docs
