import os
from celery import Celery

REDIS_URL = os.getenv(
    "CELERY_BROKER_URL",
    "redis://localhost:6379/0"
)

RESULT_BACKEND = os.getenv(
    "CELERY_RESULT_BACKEND",
    REDIS_URL
)

celery_app = Celery(
    "taskflow",
    broker=REDIS_URL,
    backend=RESULT_BACKEND,
    include=["app.worker.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Moscow",
    enable_utc=True
)