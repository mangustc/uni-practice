from typing import Optional
from pydantic import BaseModel


class AddCategoryRoot(BaseModel):
    name: str


class AddCategory(BaseModel):
    name: str
    category_name_parent: Optional[str]


class CategoryResponse(BaseModel):
    category_id: int
    category_name: str
    category_parent_id: Optional[int]

    class Config:
        orm_mode = True
