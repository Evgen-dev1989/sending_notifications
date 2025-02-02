from typing import List

import requests
from fastapi import FastAPI, HTTPException

from base_model import Model
from start import get_by_id, main
from tasks import send_notification_task

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