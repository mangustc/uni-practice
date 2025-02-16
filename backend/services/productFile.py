import json
import os
from datetime import date, timedelta, datetime
from typing import Sequence
from fastapi import UploadFile, HTTPException, status, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import joinedload, contains_eager
from database import *
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select, delete, Select, and_, or_
from schemas import *
from Function import Functions
from uuid import uuid4
import shutil


class ProductService:
    @classmethod
    async def create_product(cls, request: Request, data: CreateProduct):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут добавлять продукты"
            )
        query = select(Article).where(Article.id == data.article_id)
        async with new_session() as db:
            result = await db.execute(query)
            result = result.scalars().first()
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Такого артикула не существует",
                )
            query = select(Category).where(Category.name == data.category_name)
            result = await db.execute(query)
            result = result.scalars().first()
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Такогой категории не существует",
                )
            if data.color_name is not None:
                query = select(Color).where(Color.name == data.color_name)
                color = await db.execute(query)
                color = color.scalars().first()
                if color is None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Такого цвета не существует",
                    )
                color_id = color.id
            else:
                color_id = None
            new_product = Product(category_id=result.id, article_id=data.article_id, color_id=color_id,
                                  name=data.name, measured_in=data.measured_in,
                                  amount=data.amount, price=data.price,
                                  description=data.description, new_until=datetime.now() + timedelta(days=30))
            db.add(new_product)
            try:
                await db.commit()
                await db.refresh(new_product)
                return GetProductResponse(
                    product_id=new_product.id,
                    category_id=new_product.category_id,
                    article_id=new_product.article_id,
                    color_id=color_id,
                    product_name=new_product.name,
                    product_description=new_product.description,
                    product_measured_in=new_product.measured_in,
                    product_amount=new_product.amount,
                    product_price=new_product.price,
                    product_new=new_product.new,
                    product_hit=new_product.hit,
                    product_promotion=new_product.promotion,
                    product_percent_promotion=new_product.percent_promotion,
                    product_new_price=new_product.new_price
                )
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось добавить продукт",
                )

    @classmethod
    async def get_product(cls, product_id: int):
        query = select(Product).options(
            joinedload(Product.category),
            joinedload(Product.color)).where(Product.id == product_id)
        async with new_session() as db:
            result = await db.execute(query)
        product_field = result.scalars().first()
        if not product_field:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден"
            )

        return GetProductResponseWithNames(
            product_id=product_field.id,
            category_id=product_field.category_id,
            category_name=product_field.category.name,
            article_id=product_field.article_id,
            color_id=product_field.color_id,
            color_name=product_field.color.name if product_field.color else None,
            product_name=product_field.name,
            product_description=product_field.description,
            product_measured_in=product_field.measured_in,
            product_amount=product_field.amount,
            product_price=product_field.price,
            product_new=product_field.new,
            product_hit=product_field.hit,
            product_promotion=product_field.promotion,
            product_percent_promotion=product_field.percent_promotion,
            product_new_price=product_field.new_price
        )

    @classmethod
    async def get_product_for_page(cls, product_id: int):
        query = select(Product).options(
            joinedload(Product.category),
            joinedload(Product.color),
            joinedload(Product.characteristics)
            .joinedload(Characteristic.property)).where(Product.id == product_id)
        async with new_session() as db:
            result = await db.execute(query)
            product_field = result.scalars().first()
            query = select(Product).where(Product.article_id == product_field.article_id)
            result = await db.execute(query)
            product_fields = result.scalars().all()

        if not product_field:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден"
            )

        characteristics = []
        for characteristic in product_field.characteristics:
            characteristics.append(GetCharacteristicResponse(property_id=characteristic.property_id,
                                                             property_name=characteristic.property.name,
                                                             property_value=characteristic.property_value))
        products_by_article = []
        for prod in product_fields:
            products_by_article.append(ProductInfo(product_id=prod.id, name=prod.name))
        return GetProductForPageResponse(
            product_id=product_field.id,
            category_id=product_field.category_id,
            category_name=product_field.category.name,
            article_id=product_field.article_id,
            color_id=product_field.color_id,
            color_name=product_field.color.name if product_field.color else None,
            product_name=product_field.name,
            product_description=product_field.description,
            product_measured_in=product_field.measured_in,
            product_amount=product_field.amount,
            product_price=product_field.price,
            product_new=product_field.new,
            product_hit=product_field.hit,
            product_promotion=product_field.promotion,
            product_percent_promotion=product_field.percent_promotion,
            product_new_price=product_field.new_price,
            get_products_by_article=products_by_article,
            characteristics=characteristics
        )

    @classmethod
    async def get_all_products(cls) -> List[GetProductResponse]:  # Add return type hint
        query = select(Product).options(joinedload(Product.category), joinedload(Product.color))
        async with new_session() as db:
            result = await db.execute(query)
            products = result.scalars().all()

        product_list: List[GetProductResponse] = []
        for p in products:
            product_list.append(
                GetProductResponseWithNames(
                    product_id=p.id,
                    category_id=p.category_id,
                    category_name=p.category.name,
                    article_id=p.article_id,
                    color_id=p.color_id,
                    color_name=p.color.name if p.color else None,
                    product_name=p.name,
                    product_description=p.description,
                    product_measured_in=p.measured_in,
                    product_amount=p.amount,
                    product_price=p.price,
                    product_new=p.new,
                    product_hit=p.hit,
                    product_promotion=p.promotion,
                    product_percent_promotion=p.percent_promotion,
                    product_new_price=p.new_price
                )
            )

        return product_list

    @classmethod
    async def get_products_by_category_name(cls, category_name: str):
        query = select(Category).where(Category.name == category_name)
        async with new_session() as db:
            result = await db.execute(query)
        result = result.scalars().first()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Категория с таким названием не найдена"
            )

        category_ids = []
        categories = [result]
        while len(categories) != 0:
            temp = [elem.id for elem in categories]
            category_ids.extend(temp)
            query = select(Category).where(Category.parent_id.in_(temp))
            async with new_session() as db:
                result = await db.execute(query)
            categories = result.scalars().all()
        query = select(Product).options(
            joinedload(Product.category),
            joinedload(Product.color)).where(Product.category_id.in_(category_ids))
        async with new_session() as db:
            result = await db.execute(query)
        result = result.scalars().all()

        return [GetProductResponseWithNames(
            product_id=p.id,
            category_id=p.category_id,
            category_name=p.category.name,
            article_id=p.article_id,
            color_id=p.color_id,
            color_name=p.color.name if p.color else None,
            product_name=p.name,
            product_description=p.description,
            product_measured_in=p.measured_in,
            product_amount=p.amount,
            product_price=p.price,
            product_new=p.new,
            product_hit=p.hit,
            product_promotion=p.promotion,
            product_percent_promotion=p.percent_promotion,
            product_new_price=p.new_price
        ).__dict__ for p in result
        ]

    @classmethod
    async def get_product_photo(cls, product_id: int):
        query = select(Product).where(Product.id == product_id)
        async with new_session() as db:
            result = await db.execute(query)
        product_field = result.scalars().first()
        if not product_field:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден"
            )
        if product_field.image_path is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Изображение продукта не было найдено"
            )
        return FileResponse(product_field.image_path)

    @classmethod
    async def update_product_photo(cls, request: Request, product_id: int, file: UploadFile):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут обновлять фото продукта"
            )
        if "image" not in file.content_type:
            raise HTTPException(
                status_code=500, detail="Файл не является изображением"
            )
        if file.size > 3145728:
            raise HTTPException(
                status_code=500, detail="Файл превышает размер в 3МБ"
            )

        path = f"images/{product_id}.{file.filename.split('.')[1]}"
        async with new_session() as db:
            product_field = await db.execute(
                select(Product).where(Product.id == product_id)
            )
            product_field = product_field.scalars().first()
            if product_field is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Такого продукта не существует",
                )
            if product_field.image_path is not None:
                os.remove(os.path.join(product_field.image_path))

            try:
                contents = file.file.read()
                with open(path, "wb") as f:
                    f.write(contents)
            except Exception:
                raise HTTPException(status_code=500, detail='Something went wrong')
            finally:
                file.file.close()
            product_field.image_path = path
            await db.commit()

        return {"message": f"Файл загружен {path}"}

    @classmethod
    async def update_product_information(cls, request: Request, product_id: int, data: UpdateProduct):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут обновлять информацию об артикуле"
            )

        async with new_session() as db:
            old_product = await db.execute(select(Product).where(Product.id == product_id))
            old_product = old_product.scalars().first()
            if old_product is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Такого продукта не существует",
                )
            if data.category_name is not None:
                query = select(Category).where(Category.name == data.category_name)
                cat = await db.execute(query)
                cat = cat.scalars().first()
                if cat is None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Такогой категории не существует",
                    )
            if data.article_id is not None:
                article_field = await db.execute(
                    select(Article).where(Article.id == data.article_id)
                )
                article_field = article_field.scalars().first()
                if article_field is None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Такого артикула не существует",
                    )
            if data.color_name is not None:
                query = select(Color).where(Color.name == data.color_name)
                color = await db.execute(query)
                color = color.scalars().first()
                if color is None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Такого цвета не существует",
                    )

            for field in data.__fields__.keys():
                if getattr(data, field) is not None:
                    if field == "category_name":
                        old_product.category_id = cat.name
                        continue
                    if field == "color_name":
                        old_product.color_id = color.id
                        continue
                    setattr(old_product, field, getattr(data, field))
            if data.set_description_null:
                old_product.description = None
            if data.set_color_null:
                old_product.color_id = None
            try:
                await db.commit()
                await db.refresh(old_product)
                return GetProductResponse(
                    product_id=old_product.id,
                    category_id=old_product.category_id,
                    article_id=old_product.article_id,
                    color_id=old_product.color_id,
                    product_name=old_product.name,
                    product_description=old_product.description,
                    product_measured_in=old_product.measured_in,
                    product_amount=old_product.amount,
                    product_price=old_product.price,
                    product_new=old_product.new,
                    product_hit=old_product.hit,
                    product_promotion=old_product.promotion,
                    product_percent_promotion=old_product.percent_promotion,
                    product_new_price=old_product.new_price
                )
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось обновить информацию о продукте",
                )

    @classmethod
    async def add_characteristic(cls, request: Request, product_id: int, data: AddCharacteristic):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут добавлять характеристики"
            )

        query = select(Product).options(
            joinedload(Product.characteristics)
            .joinedload(Characteristic.property)).where(Product.id == product_id)
        async with new_session() as db:
            product = await db.execute(query)
            product = product.scalars().first()
            if product is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Продукта с таким id не существует",
                )
            query = select(Property).where(Property.name == data.property_name)
            property_field = await db.execute(query)
            property_field = property_field.scalars().first()
            if property_field is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Свойства с таким именем не существует",
                )
            for characteristic in product.characteristics:
                if characteristic.property.name == data.property_name:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="У продукта уже есть характеристика с таким свойством",
                    )
            new_characteristic = Characteristic(
                product_id=product_id,
                property_id=property_field.id,
                property_value=data.property_value
            )
            db.add(new_characteristic)
            try:
                await db.commit()
                await db.refresh(new_characteristic)
                return AddCharacteristicResponse(product_id=product_id,
                                                 property_id=property_field.id,
                                                 property_value=data.property_value)
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось добавить характеристику",
                )

    @classmethod
    async def get_characteristics_by_product_id(cls, product_id: int):
        query = select(Characteristic).options(
            joinedload(Characteristic.property)).where(Characteristic.product_id == product_id)
        async with new_session() as db:
            result = await db.execute(query)
        characteristics = result.scalars().all()
        return [GetCharacteristicResponse(
            property_id=c.property_id,
            property_name=c.property.name,
            property_value=c.property_value,
        ).__dict__ for c in characteristics
        ]

    @classmethod
    async def update_characteristic(cls, request: Request, product_id: int, data: AddCharacteristic):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут изменять характеристики"
            )
        query = select(Characteristic).join(Property).where(
            and_(Characteristic.product_id == product_id, Property.name == data.property_name))
        async with new_session() as db:
            result = await db.execute(query)
            characteristic = result.scalars().first()
            if characteristic is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Продукта/характеристики с указанными значениями не существует"
                )
            characteristic.property_value = data.property_value
            try:
                await db.commit()
                await db.refresh(characteristic)
                return AddCharacteristicResponse(
                    product_id=characteristic.product_id,
                    property_id=characteristic.property_id,
                    property_value=characteristic.property_value
                )
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось обновить информацию об характеристике",
                )

    @classmethod
    async def delete_characteristic_by_property_name(cls, request: Request, product_id: int, property_name: str):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут удалять характеристики"
            )
        query = select(Characteristic).join(Property).where(
            and_(Characteristic.product_id == product_id, Property.name == property_name))
        async with new_session() as db:
            result = await db.execute(query)
            result = result.scalars().first()
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Артикула/характеристики с указанными значениями не существует"
                )
            await db.delete(result)
            try:
                await db.commit()
                return {"message": "Характеристика успешна удалёна"}
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось удалить характеристику",
                )

    @classmethod
    async def delete_product(cls, request: Request, product_id: int):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут удалять продукты"
            )

        async with new_session() as db:
            product_field = await db.get(Product, product_id)
            if not product_field:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден"
                )
            if product_field.image_path is not None:
                os.remove(os.path.join(product_field.image_path))
            await db.delete(product_field)  # Correct delete
            try:
                await db.commit()
                return {"message": "Продукт успешно удалён"}  # Правильный формат
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось удалить продукт",
                )

    @classmethod
    async def change_wishlist_state(cls, request: Request, product_id: int):
        user_data = await Functions.get_user_data(request)
        query = select(Wishlist).where(
            and_(Wishlist.user_id == user_data["user_id"], Wishlist.product_id == product_id))
        async with new_session() as db:
            result = await db.execute(query)
            result = result.scalars().first()
            if result is not None:
                await db.delete(result)
                try:
                    await db.commit()
                    return {"message": "Продукт убран из избранного"}  # Правильный формат
                except IntegrityError:
                    await db.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось убрать продукт из избранного",
                    )
            query = select(Product).where(Product.id == product_id)
            result = await db.execute(query)
            result = result.scalars().first()
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Продукт не найден",
                )
            field = Wishlist(user_id=user_data["user_id"], product_id=product_id)
            db.add(field)
            try:
                await db.commit()
                return {"message": "Продукт добавлен в избранное"}  # Правильный формат
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось добавить продукт в избранное",
                )

    # @classmethod
    # async def place_order(cls, request: Request):
    #     user_data = await Functions.get_user_data(request)
    #     user_id = user_data["user_id"]
    #     total_amount = 0.0
    #     items_info = []
    #
    #     async with new_session() as db:
    #         cart_items = await db.execute(select(Cart).where(Cart.user_id == user_id))
    #         cart_items = cart_items.scalars().all()
    #
    #         if not cart_items:
    #             raise HTTPException(
    #                 status_code=status.HTTP_400_BAD_REQUEST,
    #                 detail="Корзина пуста"
    #             )
    #
    #         # Рассчитываем общую сумму заказа и обновляем количество товара
    #         for item in cart_items:
    #             product = await db.execute(
    #                 select(Product).options(joinedload(Product.article)).where(Product.id == item.product_id))
    #             product = product.scalars().first()
    #
    #             if not product:
    #                 raise HTTPException(
    #                     status_code=status.HTTP_404_NOT_FOUND,
    #                     detail=f"Продукт с ID {item.product_id} не найден"
    #                 )
    #
    #             # Check if article is loaded
    #             if not product.article:
    #                 raise HTTPException(
    #                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                     detail=f"Не удалось загрузить статью для продукта с ID {item.product_id}"
    #                 )
    #
    #             # Определяем цену товара (со скидкой или без)
    #             if product.new_price is not None:
    #                 price = product.new_price
    #             else:
    #                 price = product.article.price
    #
    #             total_amount += price * item.amount
    #             items_info.append({"product_id": product.id, "quantity": item.amount})
    #
    #             # Уменьшаем количество товара
    #             product.amount -= item.amount
    #             if product.amount < 0:
    #                 raise HTTPException(
    #                     status_code=status.HTTP_400_BAD_REQUEST,
    #                     detail=f"Недостаточное количество товара  {product.name}"
    #                 )
    #
    #         # Создаем запись о заказе
    #         new_order = Order(user_id=user_id, total_amount=total_amount, items=json.dumps(items_info))
    #         db.add(new_order)
    #         await db.commit()
    #         await db.refresh(new_order)
    #
    #         # Очищаем корзину пользователя
    #         for item in cart_items:
    #             await db.delete(item)
    #         await db.commit()
    #
    #         return {"order_id": new_order.id, "total_amount": total_amount,
    #                 "message": "Заказ успешно создан, ожидается оплата"}

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
    async def set_product_new(cls, request: Request, product_id: int, is_new: bool):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут изменять статус новинки"
            )

        async with new_session() as db:
            product = await db.get(Product, product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден"
                )

            product.new = is_new

            try:
                await db.commit()
                await db.refresh(product)
                return {"message": f"Статус новинки для продукта {product_id} изменен на {is_new}"}
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось изменить статус новинки",
                )

    @classmethod
    async def set_product_hit(cls, request: Request, product_id: int, is_hit: bool):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут изменять статус хита продаж"
            )

        async with new_session() as db:
            product = await db.get(Product, product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден"
                )

            product.hit = is_hit

            try:
                await db.commit()
                await db.refresh(product)
                return {"message": f"Статус хита продаж для продукта {product_id} изменен на {is_hit}"}
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось изменить статус хита продаж",
                )

    @classmethod
    async def check_and_reset_hit_status(cls):
        async with new_session() as db:
            print("Checking for expired 'hit' products...")  # Added logging
            products = await db.execute(select(Product).where(Product.hit == True))
            products = products.scalars().all()
            print(f"Found {len(products)} hit products.")

            for product in products:
                if product.last_hit_date and datetime.utcnow() - product.last_hit_date > timedelta(days=30):
                    product.hit = False
                    product.last_hit_date = None
                    print(f"Deactivating product {product.id}")

            try:
                await db.commit()
                print("Deactivated expired 'hit' products.")
            except SQLAlchemyError as e:
                await db.rollback()
                print(f"Error deactivating expired 'hit' products: {e}")

    @classmethod
    async def set_product_promotion(
            cls, request: Request, product_id: int, is_promotion: bool, percent_promotion: float
    ):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут изменять статус акции"
            )

        async with new_session() as db:
            product = await db.get(Product, product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден"
                )

            if is_promotion:
                if percent_promotion is None or not 0 < percent_promotion <= 100:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Процент скидки должен быть указан в диапазоне от 1 до 100",
                    )

                old_price = float(product.price)
                discount_amount = old_price * (percent_promotion / 100)
                new_price = old_price - discount_amount

                product.promotion = is_promotion
                product.percent_promotion = percent_promotion
                product.new_price = new_price  # Store the discounted price
            else:
                product.promotion = is_promotion
                product.percent_promotion = None
                product.new_price = None  # Reset the discounted price

            try:
                await db.commit()
                await db.refresh(product)
                return {"message": f"Статус акции для продукта {product_id} изменен на {is_promotion}"}
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось изменить статус акции",
                )

    @classmethod
    async def get_promotion_products(cls):
        query = select(Product).options(
            joinedload(Product.category),
            joinedload(Product.color)).where(Product.promotion == True)
        async with new_session() as db:
            result = await db.execute(query)
        products = result.scalars().all()

        return [GetProductResponseWithNames(
                    product_id=p.id,
                    category_id=p.category_id,
                    category_name=p.category.name,
                    article_id=p.article_id,
                    color_id=p.color_id,
                    color_name=p.color.name if p.color else None,
                    product_name=p.name,
                    product_description=p.description,
                    product_measured_in=p.measured_in,
                    product_amount=p.amount,
                    product_price=p.price,
                    product_new=p.new,
                    product_hit=p.hit,
                    product_promotion=p.promotion,
                    product_percent_promotion=p.percent_promotion,
                    product_new_price=p.new_price
                ).__dict__ for p in products
        ]

    @classmethod
    async def get_new_products(cls):
        query = select(Product).options(
            joinedload(Product.category),
            joinedload(Product.color)).where(Product.new == True)
        async with new_session() as db:
            result = await db.execute(query)
        products = result.scalars().all()

        return [GetProductResponseWithNames(
                    product_id=p.id,
                    category_id=p.category_id,
                    category_name=p.category.name,
                    article_id=p.article_id,
                    color_id=p.color_id,
                    color_name=p.color.name if p.color else None,
                    product_name=p.name,
                    product_description=p.description,
                    product_measured_in=p.measured_in,
                    product_amount=p.amount,
                    product_price=p.price,
                    product_new=p.new,
                    product_hit=p.hit,
                    product_promotion=p.promotion,
                    product_percent_promotion=p.percent_promotion,
                    product_new_price=p.new_price
                ).__dict__ for p in products
                ]

    @classmethod
    async def get_hit_products(cls):
        query = select(Product).options(
            joinedload(Product.category),
            joinedload(Product.color)).where(Product.hit == True)
        async with new_session() as db:
            result = await db.execute(query)
        products = result.scalars().all()

        return [GetProductResponseWithNames(
                    product_id=p.id,
                    category_id=p.category_id,
                    category_name=p.category.name,
                    article_id=p.article_id,
                    color_id=p.color_id,
                    color_name=p.color.name if p.color else None,
                    product_name=p.name,
                    product_description=p.description,
                    product_measured_in=p.measured_in,
                    product_amount=p.amount,
                    product_price=p.price,
                    product_new=p.new,
                    product_hit=p.hit,
                    product_promotion=p.promotion,
                    product_percent_promotion=p.percent_promotion,
                    product_new_price=p.new_price
                ).__dict__ for p in products
                ]

# @classmethod
#   async def set_product_new1(cls, request: Request, product_id: int, is_new: bool):
#       user_data = await Functions.get_user_data(request)
#       if user_data["user_role"] != "Админ":
#           raise HTTPException(
#               status_code=403, detail="Только администраторы могут изменять статус новинки"
#           )
#
#       async with new_session() as db:
#           product = await db.get(Product, product_id)
#           if not product:
#               raise HTTPException(
#                   status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден"
#               )
#
#           product.new = is_new
#           if is_new:
#               product.new_until = datetime.now() + timedelta(minutes=1)  # Save datetime
#           else:
#               product.new_until = None
#
#           try:
#               await db.commit()
#               await db.refresh(product)
#               return {"message": f"Статус новинки для продукта {product_id} изменен на {is_new}"}
#           except IntegrityError:
#               await db.rollback()
#               raise HTTPException(
#                   status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                   detail="Не удалось изменить статус новинки",
#               )
