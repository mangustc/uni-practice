from pydantic import BaseModel


class CreateArticle(BaseModel):
    subcategory_name: str
    description: str
    country: str
    price: int


class UpdateArticleCharacteristics(BaseModel):
    characteristic_color: str
    characteristic_width: str
    characteristic_density: str
    characteristic_consist: str

class ArticleResponse(BaseModel):
    article_id: int
