from typing import Optional, List
from pydantic import BaseModel

class ContactBase(BaseModel):
    office_phone: Optional[str] = None
    office_email: Optional[str] = None
    office_workhours: Optional[str] = None # Добавлено
    sales_phone: Optional[str] = None
    sales_email: Optional[str] = None
    purchase_phone: Optional[str] = None
    purchase_email: Optional[str] = None
    purchase_extension: Optional[str] = None  # For "Отдел закупок"
    purchase_addition: Optional[str] = None # Добавлено
    commercial_email: Optional[str] = None  # "Для коммерческих предложений"
    general_email: Optional[str] = None # "Общие вопросы"
    legal_address: Optional[str] = None
    ogrn: Optional[str] = None
    inn: Optional[str] = None
    kpp: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class ContactResponse(ContactBase):
    id: int
    office_phone: Optional[str] = None
    office_email: Optional[str] = None
    office_workhours: Optional[str] = None  # Добавлено
    sales_phone: Optional[str] = None
    sales_email: Optional[str] = None
    purchase_phone: Optional[str] = None
    purchase_email: Optional[str] = None
    purchase_extension: Optional[str] = None  # For "Отдел закупок"
    purchase_addition: Optional[str] = None  # Добавлено
    commercial_email: Optional[str] = None  # "Для коммерческих предложений"
    general_email: Optional[str] = None  # "Общие вопросы"
    legal_address: Optional[str] = None
    ogrn: Optional[str] = None
    inn: Optional[str] = None
    kpp: Optional[str] = None

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, contact):
        return cls(
            id=contact.id,
            office_phone=contact.office_phone,
            office_email=contact.office_email,
            office_workhours=contact.office_workhours,
            sales_phone=contact.sales_phone,
            sales_email=contact.sales_email,
            purchase_phone=contact.purchase_phone,
            purchase_email=contact.purchase_email,
            purchase_extension=contact.purchase_extension,
            purchase_addition=contact.purchase_addition,
            commercial_email=contact.commercial_email,
            general_email=contact.general_email,
            legal_address=contact.legal_address,
            ogrn=contact.ogrn,
            inn=contact.inn,
            kpp=contact.kpp,
        )

class Message(BaseModel):
    message: str

class OfficeContactResponse(BaseModel):
    phone: Optional[str]
    email: Optional[str]
    workhours: Optional[str]

class SalesContactResponse(BaseModel):
    phone: Optional[str]
    email: Optional[str]

class PurchaseContactResponse(BaseModel):
    phone: Optional[str]
    email: Optional[str]
    extension: Optional[str]

class CommercialContactResponse(BaseModel):
    email: Optional[str]

class GeneralContactResponse(BaseModel):
    email: Optional[str]

class RequisitesResponse(BaseModel):
    legal_address: Optional[str]
    ogrn: Optional[str]
    inn: Optional[str]
    kpp: Optional[str]