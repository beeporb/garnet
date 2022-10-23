import celery

app = celery.Celery(
    broker="redis://redis:6379/0", backend="redis://redis:6379/1"
)
