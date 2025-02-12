from typing import Optional
from pydantic import BaseModel


class SortProductByPriceResponse(BaseModel):
    product_name: str
    price: Optional[int]


class SortProductByNameResponse(BaseModel):
    product_name: str
    amount: float
