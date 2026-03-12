import sys
import os
from pathlib import Path
from celery import Celery

# ✅ Add Services/ to PYTHONPATH
BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Get Redis configuration from environment
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
BROKER_DB = os.getenv("REDIS_BROKER_DB", "0")
BACKEND_DB = os.getenv("REDIS_BACKEND_DB", "1")

celery_app = Celery(
    "worker",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/{BROKER_DB}",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}/{BACKEND_DB}",
    include=["Services.worker.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
)
