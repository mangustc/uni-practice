from typing import Optional, List, Dict
from pydantic import BaseModel
from pydantic.types import PositiveFloat, PositiveInt


class OrderCreate(BaseModel):
    items: List[Dict[int, float]]
    delivery_address: str


class OrderItem(BaseModel):
    product_id: int
    amount: float


class PlaceOrderRequest(BaseModel):
    delivery_service_id: int

    class Config:
        orm_mode = True


class PlaceOrderResponse(BaseModel):
    order_id: int
    total_amount: PositiveFloat
    message: str
