from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class FeedbackCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    comment: str

class FeedbackResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    comment: str
    created_at: datetime
    is_processed: bool

    class Config:
        from_attributes = True