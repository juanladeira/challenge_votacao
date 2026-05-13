import logging

from celery import Celery

from app.core.settings import settings

logger = logging.getLogger("worker")

celery_app = Celery(
    "normatik",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={},
)
