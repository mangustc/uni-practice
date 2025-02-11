from pydantic import BaseModel, Field
from typing_extensions import Annotated

PositiveInt = Annotated[int, Field(gt=0)]


class CreateArticle(BaseModel):
    subcategory_name: str
    description: str
    country: str
    measured_in: str
    price: PositiveInt


class UpdateArticleCharacteristics(BaseModel):
    characteristic_color: str
    characteristic_width: str
    characteristic_density: str
    characteristic_consist: str


class ArticleResponse(BaseModel):
    article_id: int
