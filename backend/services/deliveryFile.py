from fastapi import HTTPException, status, Request
from database import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from schemas import *
from Function import Functions




class DeliveryServices:
    @classmethod
    async def get_delivery_service(cls, delivery_service_id: int):
        async with new_session() as db:
            result = await db.execute(  # Await the execution
                select(DeliveryService).where(DeliveryService.id == delivery_service_id)
            )
            delivery_service = result.scalar_one_or_none()
            if not delivery_service:
                raise HTTPException(status_code=404, detail="Delivery service not found")
            return delivery_service

    @classmethod
    async def list_delivery_services(cls):
        async with new_session() as db:
            result = await db.execute(select(DeliveryService))
            delivery_services = result.scalars().all()
            return delivery_services

    @classmethod
    async def create_delivery_service(cls, request: Request, delivery_service: DeliveryServiceCreate):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Только администраторы могут создавать службы доставки"
            )

        async with new_session() as db:
            new_delivery_service = DeliveryService(**delivery_service.dict())
            db.add(new_delivery_service)
            try:
                await db.commit()
                await db.refresh(new_delivery_service)
                return new_delivery_service
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось создать службу доставки",
                )

    @classmethod
    async def update_delivery_service(cls, request: Request, delivery_id: int, delivery_update: DeliveryUpdate):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Только администраторы могут создавать службы доставки"
            )
        async with new_session() as db:
            old_delivery = await db.execute(select(DeliveryService).where(DeliveryService.id == delivery_id))
            old_delivery = old_delivery.scalars().first()
            if old_delivery is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Такого доставщика не существует",
                )
            update_data = delivery_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(old_delivery, key, value)
            try:
                await db.commit()
                await db.refresh(old_delivery)
                return DeliveryServiceResponseUpdate.from_orm(old_delivery)
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось обновить вакансию",
                )

    @classmethod
    async def delete_delivery(cls, request: Request, delivery_id: int):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут изменять статус новинки"
            )
        async with new_session() as db:
            db_delivery = await db.execute(select(DeliveryService).where(DeliveryService.id == delivery_id))
            db_delivery = db_delivery.scalars().first()
            if not db_delivery:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Вакансия не найдена"
                )

            await db.delete(db_delivery)
            try:
                await db.commit()
                return {"message": "Доставка успешно удалена"}
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось удалить вакансию",
                )