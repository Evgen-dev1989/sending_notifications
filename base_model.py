from pydantic import BaseModel, EmailStr
from typing import Optional

class model(BaseModel):
    recipient: Optional[EmailStr] = None
    message: str