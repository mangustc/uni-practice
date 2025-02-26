import datetime

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WholesaleBuyerCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    comment: str

class WholesaleBuyerResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True