from typing import Optional, List

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
    article_description: Optional[str] = None
    article_country: Optional[str] = None
    product_characteristic_color: Optional[str] = None
    article_characteristic_width: Optional[str] = None
    article_characteristic_density: Optional[str] = None
    article_characteristic_consist: Optional[str] = None
    article_measured_in: str
    article_price: PositiveInt
    product_new: bool
    product_hit: bool
    product_promotion: bool
    product_percent_promotion: Optional[int]
    product_new_price: Optional[float]


class GetProductSmallCardResponse(BaseModel):
    product_id: int
    product_name: str
    article_measured_in: str
    article_price: int
    product_new: bool
    product_hit: bool
    product_promotion: bool
    product_percent_promotion: Optional[int]
    product_new_price: Optional[float]


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


class CartItem(BaseModel):
    product_id: int
    product_name: str
    amount: int
    total_price: float


class CartResponse(BaseModel):
    items: List[CartItem]
    total_cart_price: float
