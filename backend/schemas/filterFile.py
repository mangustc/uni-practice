from typing import Optional, List
from pydantic import BaseModel
from enum import Enum
from schemas import CategoryResponse, GetCharacteristicResponse, GetColorResponse, MeasurementEnum
import re
from pydantic.types import PositiveFloat, PositiveInt
from datetime import datetime
from database import MeasurementEnum


class PropertyFilter1(BaseModel):
    property_id: PositiveInt
    property_name: str
    values: list[str]


class ProductInCatalogInfo(BaseModel):
    product_id: PositiveInt
    product_name: str
    product_measured_in: MeasurementEnum
    product_price: int
    product_new: bool
    product_hit: bool
    product_promotion: bool
    product_percent_promotion: Optional[float]
    product_new_price: Optional[float]


class CatalogPageInfo(BaseModel):
    number_of_products: int
    categories: list[CategoryResponse]
    min_price: float
    max_price: float
    colors: list[GetColorResponse]
    properties: list[PropertyFilter1]
    products: list[ProductInCatalogInfo]


class PropertyFilter(BaseModel):
    propertyID: int
    propertyValues: List[str]

class SortByEnum(str, Enum):
    price_asc = "price"
    price_desc = "-price"
    name_asc = "name"
    name_desc = "-name"
    none = "none"

class FilterByParamsEnum(str, Enum):
    new = "new"
    hit = "hit"
    promotion = "promotion"
    none = "none"

class CatalogFilters(BaseModel):
    categoryID: int
    productOnlyInStock: bool
    productPriceStart: Optional[PositiveFloat] = None
    productPriceEnd: Optional[PositiveFloat] = None
    properties: List[PropertyFilter] = []
    colors: List[int] = []
