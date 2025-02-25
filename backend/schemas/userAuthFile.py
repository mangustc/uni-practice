from pydantic import BaseModel, field_validator
from pydantic.types import PositiveInt
from typing import Optional
import re


class Registr(BaseModel):
    email: str
    password: str
    re_password: str
    number: Optional[str] = None

    @field_validator("email")
    def validate_email(cls, email):
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, email):
            raise ValueError("Некорректный email. Пример: example@email.com")
        return email

    @field_validator("number")
    def validate_number(cls, number):
        if number is not None:
            number_pattern = r"^\+7 \(\d{3}\) \d{3} \d{2} \d{2}$"
            if not re.match(number_pattern, number):
                raise ValueError("Некорректный формат номера телефона. Пример: +7 (923) 235 23 45")
        return number

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "example@email.com",
                    "password": "Password123!",
                    "re_password": "Password123!",
                    "number": "+7 (923) 235 23 45",
                }
            ]
        }
    }


class RegistrLegalEntity(BaseModel):  # Для Юр.лиц и ИП
    email: str
    organization_name: str
    INN: str
    password: str
    re_password: str
    number: Optional[str] = None

    @field_validator("email")
    def validate_email(cls, email):
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, email):
            raise ValueError("Некорректный email. Пример: example@email.com")
        return email

    @field_validator("number")
    def validate_number(cls, number):
        if number is not None:
            number_pattern = r"^\+7 \(\d{3}\) \d{3} \d{2} \d{2}$"
            if not re.match(number_pattern, number):
                raise ValueError("Некорректный формат номера телефона. Пример: +7 (923) 235 23 45")
        return number

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "example@email.com",
                    "organization_name": "ООО 'Заяц'",
                    "INN": "9729219090",
                    "password": "Password123!",
                    "re_password": "Password123!",
                    "number": "+7 (923) 235 23 45",
                }
            ]
        }
    }


class Login(BaseModel):
    email: str
    password: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "example@email.com",
                    "password": "Password123!",
                }
            ]
        }
    }


class LoginResponse(BaseModel):
    email: str
    token: str
    message: str


class RegistrResponse(BaseModel):
    user_id: PositiveInt
    email: str
    message: str


class GetUserInfoResponse(BaseModel):
    user_id: PositiveInt
    email: str
    name: Optional[str]
    surname: Optional[str]
    number: Optional[str]
    role: str



class ResetPassword(BaseModel):
    new_password: str
    re_new_password: str

