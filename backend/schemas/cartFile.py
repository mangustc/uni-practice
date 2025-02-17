from typing import Optional, List

from pydantic import BaseModel, field_validator
from pydantic.types import PositiveFloat, PositiveInt
from datetime import datetime


class CartItem(BaseModel):
    product_id: int
    product_name: str
    amount: int
    total_price: float

    @field_validator('product_name')
    def validate_product_name(cls, product_name: str) -> str:
        if len(product_name) > 100:
            raise ValueError('Product name must be less than 100 characters')
        return product_name


class CartResponse(BaseModel):
    items: List[CartItem]
    total_cart_price: float
