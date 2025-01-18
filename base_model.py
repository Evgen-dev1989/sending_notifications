from pydantic import BaseModel, EmailStr
from typing import Optional

class Model(BaseModel):
    recipient: Optional[EmailStr] = None
    message: str