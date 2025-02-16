from typing import Optional
from pydantic import BaseModel


class AddProperty(BaseModel):
    name: str


class AddColor(AddProperty):
    pass


class GetPropertyResponse(BaseModel):
    property_id: int
    property_name: str


class GetColorResponse(BaseModel):
    color_id: int
    color_name: str
