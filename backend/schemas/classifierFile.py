from typing import Optional
from pydantic import BaseModel, field_validator
import re


class AddProperty(BaseModel):
    name: str

    @field_validator('name')
    def validate_name(cls, name: str) -> str:
        if not re.match(r"^[\w\sа-яА-ЯёЁ]+$", name):
            raise ValueError('Property name cannot contain special characters')
        if len(name) > 50:
            raise ValueError('Property name must be less than 50 characters')
        return name


class AddColor(AddProperty):
    pass


class GetPropertyResponse(BaseModel):
    property_id: int
    property_name: str


class GetColorResponse(BaseModel):
    color_id: int
    color_name: str
