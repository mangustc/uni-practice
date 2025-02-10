from pydantic import BaseModel


class CreateArticle(BaseModel):
    subcategory_name: str
    description: str
    characteristics: str
    price: int


class ArticleResponse(BaseModel):
    article_id: int
