from typing import Optional, List
from pydantic import BaseModel
from enum import Enum
from schemas import CategoryResponse, GetColorResponse
from pydantic.types import PositiveFloat, PositiveInt
from datetime import datetime
from database import MeasurementEnum
from schemas.productFile import ProductInCatalogInfo


class PropertyFilter1(BaseModel):
    property_id: PositiveInt
    property_name: str
    values: list[str]


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
