from typing import Optional, List

from pydantic import BaseModel
from pydantic.types import PositiveFloat, PositiveInt
from datetime import datetime


class CartItem(BaseModel):
    product_id: int
    product_name: str
    amount: int
    total_price: float


class CartResponse(BaseModel):
    items: List[CartItem]
    total_cart_price: float
