from pydantic import BaseModel


class CreateProduct(BaseModel):
    article_id: int
    name: str
    amount: int


class ProductResponse(BaseModel):
    product_id: int
    product_name: str
