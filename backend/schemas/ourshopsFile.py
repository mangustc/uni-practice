from pydantic import BaseModel, Field
from typing import Optional

class ShopCreate(BaseModel):
    address: str = Field(..., description="Адрес магазина")
    schedule: str = Field(..., description="Расписание работы магазина")
    city: str = Field(..., description="Город магазина")

class ShopUpdate(BaseModel):
    address: Optional[str] = Field(None, description="Адрес магазина")
    schedule: Optional[str] = Field(None, description="Расписание работы магазина")
    city: Optional[str] = Field(None, description="Город магазина")

class ShopResponse(BaseModel):
    id: int
    address: str
    schedule: str
    photo_path: Optional[str]
    city: str

    class Config:
        from_attributes = True
