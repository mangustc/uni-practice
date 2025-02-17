from typing import Optional, List, Dict
from pydantic import BaseModel, field_validator
from pydantic.types import PositiveFloat, PositiveInt


class OrderCreate(BaseModel):
    items: List[Dict[int, float]]
    delivery_address: str

    @field_validator('delivery_address')
    def validate_delivery_address(cls, address: str) -> str:
        if not address.strip():
            raise ValueError('Delivery address cannot be empty')
        return address


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
