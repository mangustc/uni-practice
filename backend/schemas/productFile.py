from typing import Optional, List

from pydantic import BaseModel
from pydantic.types import PositiveFloat, PositiveInt
from datetime import datetime


class CreateProduct(BaseModel):
    category_name: str
    article_id: int
    name: str
    measured_in: str
    amount: PositiveFloat
    price: PositiveInt
    description: Optional[str]
    color_name: Optional[str]


class UpdateProduct(BaseModel):
    category_name: Optional[str]
    article_id: Optional[int]
    name: Optional[str]
    measured_in: Optional[str]
    amount: Optional[PositiveFloat]
    price: Optional[PositiveInt]
    description: Optional[str]
    color_name: Optional[str]
    set_description_null: bool = False
    set_color_null: bool = False


class AddCharacteristic(BaseModel):
    property_name: str
    property_value: str


class AddCharacteristicResponse(BaseModel):
    product_id: int
    property_id: int
    property_value: str


class GetCharacteristicResponse(BaseModel):
    property_id: int
    property_name: str
    property_value: str


class GetProductResponse(BaseModel):
    product_id: int
    category_id: int
    article_id: int
    color_id: Optional[int] = None
    product_name: str
    product_description: Optional[str] = None
    product_measured_in: str
    product_amount: PositiveFloat
    product_price: PositiveInt
    product_new: bool
    product_hit: bool
    product_promotion: bool
    product_percent_promotion: Optional[int] = None
    product_new_price: Optional[float] = None


class GetProductResponseWithNames(GetProductResponse):
    category_name: str
    color_name: Optional[str] = None


class ProductInfo(BaseModel):
    product_id: int
    name: str


class GetProductForPageResponse(BaseModel):
    category_id: int
    category_name: str
    article_id: int
    color_id: Optional[int] = None
    color_name: Optional[str] = None
    product_name: str
    product_description: Optional[str] = None
    product_measured_in: str
    product_amount: PositiveFloat
    product_price: PositiveInt
    product_new: bool
    product_hit: bool
    product_promotion: bool
    product_percent_promotion: Optional[int] = None
    product_new_price: Optional[float] = None
    get_products_by_article: list[ProductInfo]
    characteristics: list[GetCharacteristicResponse]


class DeliveryServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: PositiveFloat


class DeliveryServiceCreate(DeliveryServiceBase):
    pass


class DeliveryServiceResponse(DeliveryServiceBase):
    id: int

    class Config:
        orm_mode = True

#
#
# class PlaceOrderResponse(BaseModel):
#     order_id: int
#     total_amount: PositiveFloat
#     message: str


class PayOrderResponse(BaseModel):
    message: str
    order_id: int


class OrderHistoryResponse(BaseModel):
    order_id: int
    order_date: datetime
    total_amount: PositiveFloat
    payment_status: str
