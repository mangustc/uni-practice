from fastapi import HTTPException, status, Request
from database import new_session, Property, PropertyValue, Characteristic
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, and_, delete
from schemas import *
from Function import Functions


class CharacteristicService:
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
    async def add_property_value(cls, property_value: AddPropertyValue, request: Request):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут добавлять значения для свойств"
            )

        async with new_session() as db:
            query = select(Property).where(Property.name == property_value.property_name)
            result = await db.execute(query)
            result = result.scalars().first()
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Свойства с таким названием не существует",
                )
            result2 = await db.execute(
                select(PropertyValue).where(and_(PropertyValue.name == property_value.name,
                                                 PropertyValue.property_id == result.id))
            )
            if result2.scalars().first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="значение с таким именем уже существует",
                )

            new_property_value = PropertyValue(name=property_value.name, property_id=result.id)
            db.add(new_property_value)
            try:
                await db.commit()
                await db.refresh(new_property_value)
                return GetPropertyValueResponse(property_value_id=new_property_value.id,
                                                property_id=new_property_value.property_id,
                                                property_value_name=new_property_value.name)
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось добавить значение",
                )

    @classmethod
    async def get_property_values_by_property_name(cls, property_name: str):
        query = select(Property).where(Property.name == property_name)
        async with new_session() as db:
            result = await db.execute(query)
            result = result.scalars().first()
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Свойство не найдено"
                )
            query = select(PropertyValue).where(PropertyValue.property_id == result.id)
            values = await db.execute(query)
            values = values.scalars().all()
            return [GetPropertyValueResponse(
                property_value_id=v.id,
                property_id=v.property_id,
                property_value_name=v.name
            ).__dict__ for v in values
            ]

    @classmethod
    async def get_property_by_property_value_name(cls, property_value_name: str):
        query = select(PropertyValue).where(PropertyValue.name == property_value_name)
        async with new_session() as db:
            result = await db.execute(query)
            result = result.scalars().first()
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Значение не найдено"
                )
            query = select(Property).where(Property.id == result.property_id)
            result2 = await db.execute(query)
            result2 = result2.scalars().first()
            return GetPropertyResponse(property_id=result2.id, property_name=result2.name)

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
    async def get_property_value(cls, property_value_id: int):
        async with new_session() as db:
            result = await db.execute(select(PropertyValue).where(PropertyValue.id == property_value_id))
        result = result.scalars().first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Значение не найдено"
            )
        return GetPropertyValueResponse(property_value_id=result.id,
                                        property_id=result.property_id,
                                        property_value_name=result.name)

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
    async def get_all_property_values(cls):
        async with new_session() as db:
            result = await db.execute(select(PropertyValue))
            property_values = result.scalars().all()
            return [GetPropertyValueResponse(
                property_value_id=p.id,
                property_id=p.property_id,
                property_value_name=p.name
            ).__dict__ for p in property_values
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
    async def update_property_value(cls, property_value_id: int, new_name: str, request: Request):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут изменять значения свойств"
            )

        async with new_session() as db:
            result = await db.get(PropertyValue, property_value_id)
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Свойство не найдено"
                )

            # Check if the new name already exists for another property
            existing_property = await db.execute(
                select(PropertyValue).where(
                    and_(PropertyValue.name == new_name, PropertyValue.id != property_value_id)
                )
            )
            if existing_property.scalars().first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Значение с таким именем уже существует",
                )

            result.name = new_name  # Correct update
            try:
                await db.commit()
                await db.refresh(result)
                return GetPropertyValueResponse(property_value_id=result.id,
                                                property_id=result.property_id,
                                                property_value_name=result.name)
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось обновить значение",
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
    async def delete_property_value(cls, property_value_id: int, request: Request):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут удалять значения свойств"
            )
        query = delete(PropertyValue).where(PropertyValue.id == property_value_id).returning(PropertyValue.id)
        async with new_session() as db:
            result = await db.execute(query)
            if result.scalars().first() is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Значение не найдено"
                )
            try:
                await db.commit()
                return {"message": "Значение успешно удалёно"}
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось удалить значение",
                )
