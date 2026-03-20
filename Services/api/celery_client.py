"""
Celery client for the API — imports the shared app and exposes task signatures
without running a worker. The API uses .delay() / .apply_async() only.
"""
from celery import Celery
from services.api.config import get_settings

settings = get_settings()

celery_app = Celery(
    "api_client",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
)
