from fastapi import FastAPI, HTTPException
from base_model import Model
from send_email import send_notification

app = FastAPI()

@app.post("/notify/")
async def notify(notification: Model):
    result = send_notification(
        recipient=notification.recipient,
        message=notification.message
    )
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result
