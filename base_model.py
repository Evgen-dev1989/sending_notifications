from typing import Optional

from pydantic import BaseModel, EmailStr


class Model(BaseModel):
    email: Optional[EmailStr] = None
    message: str
    id: int