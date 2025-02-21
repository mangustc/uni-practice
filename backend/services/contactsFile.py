from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from schemas  import ContactCreate, ContactUpdate, ContactResponse, Message
from database import new_session, Contact as ContactModel
from typing import Dict, Any


class ContactService:
    @classmethod
    async def create_contact(cls, contact: ContactCreate) -> ContactResponse:
        async with new_session() as db:
            db_contact = ContactModel(**contact.dict())
            db.add(db_contact)
            try:
                await db.commit()
                await db.refresh(db_contact)
                return ContactResponse.from_orm(db_contact)
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось добавить контакт",
                )

    @classmethod
    async def get_contacts(cls) -> list[ContactResponse]:
        async with new_session() as db:
            contacts = await db.execute(select(ContactModel))
            return [ContactResponse.from_orm(contact) for contact in contacts.scalars().all()]

    @classmethod
    async def get_contact(cls, contact_id: int) -> ContactResponse:
        async with new_session() as db:
            result = await db.execute(select(ContactModel).where(ContactModel.id == contact_id))
            db_contact = result.scalars().first()
            if not db_contact:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Контакт не найден"
                )
            return ContactResponse.from_orm(db_contact)

    @classmethod
    async def update_contact(
        cls, contact_id: int, contact_update: ContactUpdate
    ) -> ContactResponse:
        async with new_session() as db:
            result = await db.execute(select(ContactModel).where(ContactModel.id == contact_id))
            db_contact = result.scalars().first()

            if not db_contact:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Контакт не найден"
                )

            update_data = contact_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_contact, key, value)

            try:
                await db.commit()
                await db.refresh(db_contact)
                return ContactResponse.from_orm(db_contact)
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось обновить контакт",
                )

    @classmethod
    async def delete_contact(cls, contact_id: int) -> Message:
        async with new_session() as db:
            result = await db.execute(select(ContactModel).where(ContactModel.id == contact_id))
            db_contact = result.scalars().first()

            if not db_contact:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Контакт не найден"
                )

            await db.delete(db_contact)
            try:
                await db.commit()
                return Message(message="Контакт успешно удален")
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось удалить контакт",
                )

    @classmethod
    async def get_office_contact(cls) -> Dict[str, Any]:
        async with new_session() as db:
            result = await db.execute(select(ContactModel))
            contact = result.scalars().first()

            if not contact:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Контакт не найден")

            return {
                "phone": contact.office_phone,
                "email": contact.office_email,
                "workhours": contact.office_workhours,
            }

    @classmethod
    async def get_sales_contact(cls) -> Dict[str, str]:
        async with new_session() as db:
            result = await db.execute(select(ContactModel))
            contact = result.scalars().first()

            if not contact:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Контакт не найден")

            return {
                "phone": contact.sales_phone,
                "email": contact.sales_email,
            }

    @classmethod
    async def get_purchase_contact(cls) -> Dict[str, str]:
        async with new_session() as db:
            result = await db.execute(select(ContactModel))
            contact = result.scalars().first()

            if not contact:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Контакт не найден")

            return {
                "phone": contact.purchase_phone,
                "email": contact.purchase_email,
                "extension": contact.purchase_extension,
            }

    @classmethod
    async def get_commercial_contact(cls) -> Dict[str, str]:
        async with new_session() as db:
            result = await db.execute(select(ContactModel))
            contact = result.scalars().first()

            if not contact:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Контакт не найден")

            return {
                "email": contact.commercial_email,
            }

    @classmethod
    async def get_general_contact(cls) -> Dict[str, str]:
        async with new_session() as db:
            result = await db.execute(select(ContactModel))
            contact = result.scalars().first()

            if not contact:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Контакт не найден")

            return {
                "email": contact.general_email,
            }

    @classmethod
    async def get_requisites(cls) -> Dict[str, str]:
        async with new_session() as db:
            result = await db.execute(select(ContactModel))
            contact = result.scalars().first()

            if not contact:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Контакт не найден")

            return {
                "legal_address": contact.legal_address,
                "ogrn": contact.ogrn,
                "inn": contact.inn,
                "kpp": contact.kpp,
            }


