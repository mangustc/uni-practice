from typing import Optional
from pydantic import BaseModel


class AddProperty(BaseModel):
    name: str


class AddPropertyValue(BaseModel):
    name: str
    property_name: str


class GetPropertyResponse(BaseModel):
    property_id: int
    property_name: str


class GetPropertyValueResponse(BaseModel):
    property_value_id: int
    property_id: int
    property_value_name: str
