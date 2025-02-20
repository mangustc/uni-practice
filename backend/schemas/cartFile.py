from typing import Optional, List
from database import MeasurementEnum
from pydantic import BaseModel, field_validator
from pydantic.types import PositiveFloat, PositiveInt
from datetime import datetime


class CartItem(BaseModel):
    product_id: PositiveInt
    article_id: PositiveInt
    product_name: str
    product_measured_in: MeasurementEnum
    product_amount: float
    product_amount_in_cart: float
    product_price: PositiveFloat
    product_percent_promotion: Optional[int]
    product_new_price: Optional[float]
    total_price: PositiveFloat

    @field_validator('product_name')
    def validate_product_name(cls, product_name: str) -> str:
        if len(product_name) > 100:
            raise ValueError('Product name must be less than 100 characters')
        return product_name


class CartResponse(BaseModel):
    items: List[CartItem]
    total_products_price: float
    total_promotion_price: float
    total_cart_price: PositiveFloat
