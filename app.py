from fastapi import FastAPI, HTTPException
import requests
from base_model import Model
from tasks import send_notification_task
from start import connect_db, main
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
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



@app.get("/notify/")

async def main():
    
    base = await connect_db()

    emails = [record['email'] for record in base]

    for i in emails:
        print(i)
    return emails
