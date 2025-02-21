from typing import List, Dict, Any

from fastapi import APIRouter, HTTPException, status

from services import ContactService
from schemas import *

router = APIRouter(tags=["Contacts"])


@router.get("/contacts/office", response_model=OfficeContactResponse)
async def get_office_contact():
    return await ContactService.get_office_contact()


@router.get("/contacts/sales", response_model=SalesContactResponse)
async def get_sales_contact():
    return await ContactService.get_sales_contact()


@router.get("/contacts/purchase", response_model=PurchaseContactResponse)
async def get_purchase_contact():
    return await ContactService.get_purchase_contact()


@router.get("/contacts/commercial", response_model=CommercialContactResponse)
async def get_commercial_contact():
    return await ContactService.get_commercial_contact()


@router.get("/contacts/general", response_model=GeneralContactResponse)
async def get_general_contact():
    return await ContactService.get_general_contact()


@router.get("/contacts/requisites", response_model=RequisitesResponse)
async def get_requisites():
    return await ContactService.get_requisites()

@router.post("/contacts/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact_endpoint(contact: ContactCreate):
    return await ContactService.create_contact(contact=contact)


@router.get("/contacts/", response_model=List[ContactResponse])
async def read_contacts():
    return await ContactService.get_contacts()


@router.get("/contacts/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int):
    return await ContactService.get_contact(contact_id=contact_id)


@router.put("/contacts/{contact_id}", response_model=ContactResponse)
async def update_contact_endpoint(contact_id: int, contact_update: ContactUpdate):
    return await ContactService.update_contact(contact_id=contact_id, contact_update=contact_update)


@router.delete("/contacts/{contact_id}", response_model=Message, status_code=status.HTTP_200_OK)
async def delete_contact_endpoint(contact_id: int):
    return await ContactService.delete_contact(contact_id=contact_id)
