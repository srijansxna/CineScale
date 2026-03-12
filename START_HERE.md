# 🚀 CineScale - Start Here

## ✅ Dependencies Installed!

All Python packages are now installed. You just need to start Redis.

## Choose Your Method:

### Method 1: Docker (Recommended - Everything in One Command)

1. **Start Docker Desktop** (look for the whale icon in your menu bar)
2. Run this command:
   ```bash
   docker compose up --build
   ```
3. Access the API at: http://localhost:8000/docs

That's it! Redis, API, and Worker all start together.

---

### Method 2: Local Development (Redis + Python)

#### Step 1: Install Redis
```bash
brew install redis
```

#### Step 2: Start Redis
```bash
brew services start redis
```

#### Step 3: Create .env file
```bash
cp .env.example .env
```

#### Step 4: Run the API
```bash
python3 run.py
```

#### Step 5: Access the API
Open: http://localhost:8000/docs

---

## 🧪 Test It Works

Once running, try:

```bash
# Health check
curl http://localhost:8000/health

# Upload a video
curl -X POST http://localhost:8000/api/upload \
  -F "file=@Services/worker/samples/demo.mp4"
```

---

## 📚 What's Available

- **API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 🐛 Troubleshooting

### "Cannot connect to Docker daemon"
→ Start Docker Desktop application

### "Connection refused to Redis"
→ Make sure Redis is running:
```bash
brew services list | grep redis
```

### Port 8000 already in use
```bash
lsof -ti:8000 | xargs kill -9
```

---

## 📖 Next Steps

1. ✅ Start the service (see above)
2. 📖 Read [QUICKSTART.md](QUICKSTART.md) for API usage
3. 🔧 Read [README_NEW.md](README_NEW.md) for detailed docs
4. 🚀 Start building!

---

## 💡 Quick Commands

```bash
# Docker method
docker compose up --build          # Start everything
docker compose logs -f api         # View logs
docker compose down                # Stop everything

# Local method
python3 run.py                     # Start API
brew services start redis          # Start Redis
brew services stop redis           # Stop Redis
```
