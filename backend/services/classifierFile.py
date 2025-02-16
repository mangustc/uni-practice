from fastapi import HTTPException, status, Request
from database import new_session, Property, Color
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, and_, delete, Select
from schemas import *
from Function import Functions


class ClassifierService:
    @classmethod
    async def add_property(cls, property_name: AddProperty, request: Request):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут добавлять свойства"
            )

        async with new_session() as db:
            result = await db.execute(
                select(Property).where(Property.name == property_name.name)
            )
            if result.scalars().first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Свойство с таким именем уже существует",
                )

            new_property = Property(name=property_name.name)
            db.add(new_property)
            try:
                await db.commit()
                await db.refresh(new_property)
                return GetPropertyResponse(property_id=new_property.id, property_name=new_property.name)
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось добавить свойство",
                )

    @classmethod
    async def add_color(cls, color_name: AddColor, request: Request):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут добавлять цвета"
            )

        async with new_session() as db:
            result = await db.execute(
                select(Color).where(Color.name == color_name.name)
            )
            if result.scalars().first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Цвет с таким именем уже существует",
                )

            new_color = Color(name=color_name.name)
            db.add(new_color)
            try:
                await db.commit()
                await db.refresh(new_color)
                return GetColorResponse(color_id=new_color.id, color_name=new_color.name)
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось добавить цвет",
                )

    @classmethod
    async def get_property(cls, property_id: int):
        async with new_session() as db:
            result = await db.execute(select(Property).where(Property.id == property_id))
        result = result.scalars().first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Свойство не найдено"
            )
        return GetPropertyResponse(property_id=result.id, property_name=result.name)

    @classmethod
    async def get_color(cls, color_id: int):
        async with new_session() as db:
            result = await db.execute(select(Color).where(Color.id == color_id))
        result = result.scalars().first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Цвет не найден"
            )
        return GetColorResponse(color_id=result.id, color_name=result.name)

    @classmethod
    async def get_all_properties(cls):
        async with new_session() as db:
            result = await db.execute(select(Property))
            properties = result.scalars().all()
            return [GetPropertyResponse(
                property_id=p.id,
                property_name=p.name
            ).__dict__ for p in properties
            ]

    @classmethod
    async def get_all_colors(cls):
        async with new_session() as db:
            result = await db.execute(select(Color))
            colors = result.scalars().all()
            return [GetColorResponse(
                color_id=c.id,
                color_name=c.name
            ).__dict__ for c in colors
            ]

    @classmethod
    async def update_property(cls, property_id: int, new_name: str, request: Request):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут изменять свойства"
            )

        async with new_session() as db:
            result = await db.get(Property, property_id)
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Свойство не найдено"
                )

            # Check if the new name already exists for another property
            existing_property = await db.execute(
                select(Property).where(
                    and_(Property.name == new_name, Property.id != property_id)
                )
            )
            if existing_property.scalars().first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Свойство с таким именем уже существует",
                )

            result.name = new_name  # Correct update
            try:
                await db.commit()
                await db.refresh(result)
                return GetPropertyResponse(property_id=result.id, property_name=result.name)
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось обновить свойство",
                )

    @classmethod
    async def update_color(cls, color_id: int, new_name: str, request: Request):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут изменять цвета"
            )

        async with new_session() as db:
            result = await db.get(Color, color_id)
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Цвет не найден"
                )

            # Check if the new name already exists for another property
            existing_property = await db.execute(
                select(Color).where(
                    and_(Color.name == new_name, Color.id != color_id)
                )
            )
            if existing_property.scalars().first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Цвет с таким именем уже существует",
                )

            result.name = new_name  # Correct update
            try:
                await db.commit()
                await db.refresh(result)
                return GetColorResponse(color_id=result.id, color_name=result.name)
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось обновить цвет",
                )

    @classmethod
    async def delete_property(cls, property_id: int, request: Request):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут удалять свойства"
            )
        query = delete(Property).where(Property.id == property_id).returning(Property.id)
        async with new_session() as db:
            result = await db.execute(query)
            if result.scalars().first() is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Свойство не найдено"
                )
            try:
                await db.commit()
                return {"message": "Свойство успешно удалёно"}
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось удалить свойство",
                )

    @classmethod
    async def delete_color(cls, color_id: int, request: Request):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут удалять цвета"
            )
        query = delete(Color).where(Color.id == color_id).returning(Color.id)
        async with new_session() as db:
            result = await db.execute(query)
            if result.scalars().first() is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Цвет не найден"
                )
            try:
                await db.commit()
                return {"message": "Цвет успешно удалён"}
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось удалить цвет",
                )
