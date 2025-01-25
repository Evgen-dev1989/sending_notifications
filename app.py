from fastapi import FastAPI, HTTPException
from base_model import Model
from tasks import send_notification_task

app = FastAPI()

@app.post("/notify/")
async def notify(notification: Model):
    task = send_notification_task.delay(
        recipient=notification.recipient,
        message=notification.message
    )
    return {"task_id": task.id, "status": "Task sent to queue"}
