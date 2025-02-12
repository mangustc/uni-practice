from pydantic import BaseModel
from typing import List, Dict


class OrderCreate(BaseModel):
    items: List[Dict[int, float]]  #Список товаров в корзине с Product_id и количеством
    delivery_address: str
