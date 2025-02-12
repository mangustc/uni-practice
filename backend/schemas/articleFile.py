from typing import Optional
from pydantic import BaseModel
from pydantic.types import PositiveInt


class CreateArticle(BaseModel):
    category_name: str
    description: Optional[str]
    country: Optional[str]
    measured_in: str
    price: PositiveInt


class GetArticleResponse(BaseModel):
    article_category_id: int
    article_description: Optional[str]
    article_country: Optional[str]
    article_measured_in: str
    article_price: int
    article_characteristic_color: Optional[str]
    article_characteristic_width: Optional[str]
    article_characteristic_density: Optional[str]
    article_characteristic_consist: Optional[str]


class UpdateArticleCharacteristics(BaseModel):
    characteristic_color: str
    characteristic_width: str
    characteristic_density: str
    characteristic_consist: str


class ArticleResponse(BaseModel):
    article_id: int
