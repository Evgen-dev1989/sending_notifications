from pydantic import BaseModel, EmailStr
from typing import Optional

class Model(BaseModel):
    email: EmailStr
    message: str