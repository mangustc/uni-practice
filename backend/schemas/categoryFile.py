from pydantic import BaseModel


class AddCategory(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    category_id: int
    category_name: str

    class Config:
        orm_mode = True
