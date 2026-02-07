import sys
from pathlib import Path
from celery import Celery

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
    include=["tasks_thumbnail", "tasks_transcode"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
)

celery_app.conf.task_routes = {
    "tasks_thumbnail.*": {"queue": "thumbnails"},
    "tasks_transcode.*": {"queue": "transcoding"},
}
