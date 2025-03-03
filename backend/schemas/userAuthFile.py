from pydantic import BaseModel, field_validator, FieldValidationInfo
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


class UpdateUserInfoRequest(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    number: Optional[str] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None

    # @field_validator("number")
    # def validate_number(cls, number):
    #     if number is not None:
    #         number_pattern = r"^\+7 \(\d{3}\) \d{3} \d{2} \d{2}$"
    #         if not re.match(number_pattern, number):
    #             raise ValueError("Некорректный формат номера телефона. Пример: +7 (923) 235 23 45")
    #     return number
    #
    # @field_validator("password")
    # def validate_password(cls, password):
    #     if password is not None:
    #         password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
    #         if not re.match(password_pattern, password):
    #             raise ValueError("Пароль должен содержать как минимум 8 символов, включая одну заглавную букву, одну строчную букву, одну цифру и один спецсимвол.")
    #     return password
    #
    # @field_validator("confirm_password", mode="after")
    # def validate_confirm_password(cls, confirm_password, info: FieldValidationInfo):
    #     if confirm_password is not None and info.data.get("password") is not None:
    #         if confirm_password != info.data["password"]:
    #             raise ValueError("Пароли не совпадают")
    #     elif confirm_password is not None and info.data.get("password") is None:
    #         raise ValueError("Для подтверждения пароля необходимо указать пароль")
    #     return confirm_password
    #
    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #                 "name": "Иван",
    #                 "surname": "Иванов",
    #                 "number": "+7 (923) 235 23 45",
    #                 "password": "Password123!",
    #                 "confirm_password": "Password123!",
    #             }
    #         ]
    #     }
    # }


class EmailData(BaseModel):
    email: str