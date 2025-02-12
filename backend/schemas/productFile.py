from typing import Optional

from pydantic import BaseModel
from pydantic.types import PositiveFloat, PositiveInt
from datetime import datetime


class CreateProduct(BaseModel):
    article_id: int
    name: str
    amount: PositiveFloat


class GetProductResponse(BaseModel):
    product_id: int
    article_id: int
    product_name: str
    product_amount: PositiveFloat
    article_description: Optional[str]
    country: Optional[str]
    characteristic_color: Optional[str]
    characteristic_width: Optional[str]
    characteristic_density: Optional[str]
    characteristic_consist: Optional[str]
    article_measured_in: str
    article_price: PositiveInt


class GetProductSmallCardResponse(BaseModel):
    product_name: str
    article_measured_in: str
    article_price: int


class ProductResponse(BaseModel):
    product_id: int
    product_name: str


class PlaceOrderResponse(BaseModel):
    order_id: int
    total_amount: PositiveFloat
    message: str


class PayOrderResponse(BaseModel):
    message: str
    order_id: int


class OrderHistoryResponse(BaseModel):
    order_id: int
    order_date: datetime
    total_amount: PositiveFloat
    payment_status: str
