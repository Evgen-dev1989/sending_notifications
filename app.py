from fastapi import FastAPI, HTTPException
import requests
from base_model import Model
from tasks import send_notification_task
from start import main, get_by_id
from typing import List

app = FastAPI()

@app.post("/notify/send_all")

async def notify(notification: Model):
    task = send_notification_task.delay(
        recipient=notification.recipient,
        message=notification.message
    )

    return {"task_id": task.id, "status": "Task sent to queue"}



@app.get("/notify/show_all")
async def main_app():
    data = await main()
    return data



@app.get("/notify/{id}")
async def get_id(id: int):
    by_id = await get_by_id(id)
    return by_id