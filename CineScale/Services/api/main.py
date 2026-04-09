from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from services.api.routes import upload, jobs, videos
from services.api.config import get_settings
from services.api.db.postgres import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    await init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(jobs.router, prefix="/api", tags=["jobs"])
app.include_router(videos.router, prefix="/api", tags=["videos"])


@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.app_name}


@app.get("/")
async def root():
    return {
        "message": "CineScale Video Processing API",
        "docs": "/docs"
    }
