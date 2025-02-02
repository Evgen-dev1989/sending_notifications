from pydantic import BaseModel, EmailStr
from typing import Optional

class Model(BaseModel):
    email: Optional[EmailStr] = None
    message: str
    id: int