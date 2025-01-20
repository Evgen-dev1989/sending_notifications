from celery_app import celery_app
from send_email import send_notification

@celery_app.task
def send_notification_task(recipient: str, message: str):
    return send_notification(recipient, message)
