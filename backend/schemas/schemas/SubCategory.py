from pydantic import BaseModel

class AddSubcategory(BaseModel):
    name: str
    category_id: int


class SubcategoryResponse(BaseModel):
    subcategory_id: int
    subcategory_name: str
    category_id: int

    class Config:
        orm_mode = True