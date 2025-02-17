from typing import Optional, List

from pydantic import BaseModel, field_validator
import re
from pydantic.types import PositiveFloat, PositiveInt
from datetime import datetime
from database import MeasurementEnum


class CreateProduct(BaseModel):
    category_name: str

    @field_validator('category_name')
    def validate_category_name(cls, name: str) -> str:
        if not re.match(r"^[\w\sа-яА-ЯёЁ]+$", name):
            raise ValueError('Category name cannot contain special characters')
        return name
    article_id: PositiveInt
    name: str

    @field_validator('name')
    def validate_product_name(cls, name: str) -> str:
        if not re.match(r"^[\w\sа-яА-ЯёЁ]+$", name):
            raise ValueError('Product name cannot contain special characters')
        if len(name) > 100:
            raise ValueError('Product name must be less than 100 characters')
        return name

    measured_in: MeasurementEnum
    amount: PositiveFloat
    price: PositiveInt
    description: Optional[str]

    @field_validator('description')
    def validate_description(cls, description: Optional[str]) -> Optional[str]:
        if description and len(description) > 255:
            raise ValueError('Description must be less than 255 characters')
        return description

    color_name: Optional[str]


class UpdateProduct(BaseModel):
    category_name: Optional[str]
    article_id: Optional[PositiveInt]
    name: Optional[str]
    measured_in: Optional[MeasurementEnum]
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
    product_id: PositiveInt
    property_id: PositiveInt
    property_value: str


class GetCharacteristicResponse(BaseModel):
    property_id: PositiveInt
    property_name: str
    property_value: str


class GetProductResponse(BaseModel):
    product_id: PositiveInt
    category_id: PositiveInt
    article_id: PositiveInt
    color_id: Optional[PositiveInt] = None
    product_name: str
    product_description: Optional[str] = None
    product_measured_in: MeasurementEnum
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
    product_id: PositiveInt
    name: str


class GetProductForPageResponse(BaseModel):
    category_id: PositiveInt
    category_name: str
    article_id: PositiveInt
    color_id: Optional[PositiveInt] = None
    color_name: Optional[str] = None
    product_name: str
    product_description: Optional[str] = None
    product_measured_in: MeasurementEnum
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
    order_id: PositiveInt


class OrderHistoryResponse(BaseModel):
    order_id: PositiveInt
    order_date: datetime
    total_amount: PositiveFloat
    payment_status: str
