from celery import Celery

celery = Celery(
    "xenyou", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0"
)

celery.conf.beat_schedule = {
    "train-recommender-daily": {
        "task": "app.tasks.recommender.train_recommender",
        "schedule": 86400.0,  # every 24h
    },
}
celery.conf.timezone = "UTC"
