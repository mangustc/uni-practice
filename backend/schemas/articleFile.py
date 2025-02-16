from typing import Optional
from pydantic import BaseModel
from pydantic.types import PositiveInt


class GetArticleResponse(BaseModel):
    article_id: int
