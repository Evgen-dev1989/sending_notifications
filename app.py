from typing import List, Optional

import requests
from fastapi import FastAPI, Form, HTTPException
from pydantic import EmailStr

from base_model import Model
from start import add_notify, get_by_id, main, update_notify
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

@app.get("/notify/show_all/{id}")
async def get_id(id: int):
    by_id = await get_by_id(id)
    return by_id

@app.post("/notify/add_notify")
async def add_form(email:Optional[EmailStr] = Form(...), message: Optional[str] = Form(...)):
    add = await add_notify(email, message)
    return "Success, mail and message added to notifications" , add

@app.put("/notify/update_notify")
async def update_form(id: int = Form(...), email:Optional[EmailStr] = Form(...), message: Optional[str] = Form(...)):
    update_by_id = await update_notify(id, email, message)
    return "Success, mail and message added to notifications" , update_by_id
    