from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",  
    backend="redis://localhost:6379/0"  
)

celery_app.conf.task_routes = {
    "tasks.send_notification_task": {"queue": "notifications"}
}
