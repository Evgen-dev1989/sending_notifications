from pydantic import BaseModel, EmailStr
from typing import Optional

class Message_model(BaseModel):
    channel: str
    recipient: Optional[EmailStr] = None
    message: str