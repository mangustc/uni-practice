from pydantic import BaseModel, Field
from typing_extensions import Annotated

PositiveFloat = Annotated[float, Field(gt=0)]


class CreateProduct(BaseModel):
    article_id: int
    name: str
    amount: PositiveFloat


class ProductResponse(BaseModel):
    product_id: int
    product_name: str
