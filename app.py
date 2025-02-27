from typing import Optional

from fastapi import FastAPI, Form, HTTPException
from pydantic import EmailStr
from fastapi.middleware.cors import CORSMiddleware

from base_model import Model
from start import add_notify, get_by_id, update_notify, get_all, del_notify
from tasks import send_notification_task

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

@app.post("/notify/send_email")
async def notify(notification: Model):
    task = send_notification_task.delay(
        email=notification.email,
        message=notification.message
    )
    return {"task_id": task.id, "status": "Task sent to queue"}



@app.get("/notify/show_all")
async def main_app():
    try:
        base = await get_all()
        data = []
        for record in base:
            info = {"id": record["id"], "email": record["email"], "message": record["message"]}
            data.append(info)

        return data
    except HTTPException as e:
        raise e  

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/notify/show_all/{id}")
async def get_id(id: int):
    try:
        record = await get_by_id(id)
        return record
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/notify/add_notify")
async def add_form(email:Optional[EmailStr] = Form(None), message: Optional[str] = Form(None)):
    try:
        add = await add_notify(email, message)
        return "Success, mail and message added to notifications" , add
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    

@app.put("/notify/update_notify")
async def update_form(data: Model):
    try:
        updated_data = await update_notify(data.id, data.email, data.message)
        return {"message": "Success, mail and message updated", "data": updated_data}

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/notify/delete_notify/{id}")
async def delete_notify(id: int):
    try:
        delete_by_id = await del_notify(id)
        return {f"notify with id: {id} successfully removed"}
    
    except HTTPException as e:
        raise e  
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.delete("/notify/delete_not/{id}")
async def delete_notify(id: int):
    try:
        delete_by_id = await del_notify(id)
        return {f"notify with id: {id} successfully removed"}
    
    except HTTPException as e:
        raise e  
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

