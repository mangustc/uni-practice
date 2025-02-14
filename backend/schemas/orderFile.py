from pydantic import BaseModel
from typing import List, Dict


class OrderCreate(BaseModel):
    items: List[Dict[int, float]]
    delivery_address: str
