import re
from typing import Optional
from pydantic import BaseModel, field_validator
from pydantic.types import PositiveInt


class AddCategoryRoot(BaseModel):
    name: str

    @field_validator('name')
    def validate_name(cls, name: str) -> str:
        if not re.match(r"^[a-zA-Z0-9\sа-яА-ЯёЁ(),]+$", name):
            raise ValueError('Category name cannot contain special characters')
        if len(name) > 50:
            raise ValueError('Category name must be less than 50 characters')
        return name


class AddCategory(BaseModel):
    name: str
    category_name_parent: Optional[str]

    @field_validator('name')
    def validate_name(cls, name: str) -> str:
        if not re.match(r"^[a-zA-Z0-9\sа-яА-ЯёЁ(),]+$", name):
            raise ValueError('Category name cannot contain special characters')
        if len(name) > 50:
            raise ValueError('Category name must be less than 50 characters')
        return name



class CategoryResponse(BaseModel):
    category_id: PositiveInt
    category_name: str
    category_parent_id: Optional[int]

    class Config:
        orm_mode = True
