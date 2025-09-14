from celery import Celery

celery_app = Celery(
    "ml_tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery_app.conf.task_routes = {
    "ml_service.tasks.train_lstm_task": {"queue": "training"},
}