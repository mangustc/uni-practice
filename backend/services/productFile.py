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

        async with new_session() as db:
            article = await db.execute(
                select(Article).where(Article.id == data.article_id)
            )
            article = article.scalars().first()
            if article is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Такого артикула не существует",
                )

            new_product = Product(article_id=data.article_id, name=data.name, amount=data.amount, new_until=datetime.now() + timedelta(days=30))
            db.add(new_product)
            try:
                await db.commit()
                await db.refresh(new_product)
                return ProductResponse(product_id=new_product.id,
                                       product_name=new_product.name)  # Return правильный формат
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось добавить продукт",
                )

    @classmethod
    async def get_product(cls, product_id: int):
        query = select(Product).options(joinedload(Product.article)).where(Product.id == product_id)
        async with new_session() as db:
            result = await db.execute(query)
        product_field = result.scalars().first()
        if not product_field:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден"
            )
        return {
            "product_id": product_field.id,
            "article_id": product_field.article_id,
            "product_name": product_field.name,
            "product_amount": product_field.amount,
            "article_description": product_field.article.description,
            "country": product_field.article.country,
            "characteristic_color": product_field.article.characteristic_color,
            "characteristic_width": product_field.article.characteristic_width,
            "characteristic_density": product_field.article.characteristic_density,
            "characteristic_consist": product_field.article.characteristic_consist,
            "article_measured_in": product_field.article.measured_in,
            "article_price": product_field.article.price
        }  # Correct format

    @classmethod
    async def get_all_products_small_card(cls):
        query = select(Product).options(joinedload(Product.article))
        async with new_session() as db:
            result = await db.execute(query)
        products = result.scalars().all()
        return [
            {
                "product_name": p.name,
                "article_measured_in": p.article.measured_in,
                "article_price": p.article.price
            } for p in products
        ]

    @classmethod
    async def get_all_products(cls):
        query = select(Product).options(joinedload(Product.article))
        async with new_session() as db:
            result = await db.execute(query)
        products = result.scalars().all()
        return [
            {"product_id": p.id,
             "article_id": p.article_id,
             "product_name": p.name,
             "product_amount": p.amount,
             "article_description": p.article.description,
             "country": p.article.country,
             "characteristic_color": p.article.characteristic_color,
             "characteristic_width": p.article.characteristic_width,
             "characteristic_density": p.article.characteristic_density,
             "characteristic_consist": p.article.characteristic_consist,
             "article_measured_in": p.article.measured_in,
             "article_price": p.article.price} for p in products
        ]  # Correct format

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
        query = select(Product).join(Article).options(contains_eager(Product.article)).where(Article.category_id.in_(category_ids))
        async with new_session() as db:
            result = await db.execute(query)
        result = result.scalars().all()

        return [
            {"product_id": p.id,
             "article_id": p.article_id,
             "product_name": p.name,
             "product_amount": p.amount,
             "article_description": p.article.description,
             "country": p.article.country,
             "characteristic_color": p.article.characteristic_color,
             "characteristic_width": p.article.characteristic_width,
             "characteristic_density": p.article.characteristic_density,
             "characteristic_consist": p.article.characteristic_consist,
             "article_measured_in": p.article.measured_in,
             "article_price": p.article.price} for p in result
        ]  # Correct format

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
    async def update_product_information(cls, request: Request, product_id: int, data: CreateProduct):
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

            article_field = await db.execute(
                select(Article).where(Article.id == data.article_id)
            )
            article_field = article_field.scalars().first()
            if article_field is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Такого артикула не существует",
                )

            old_product.category_id = data.article_id
            old_product.name = data.name
            old_product.amount = data.amount
            try:
                await db.commit()
                await db.refresh(old_product)
                return ProductResponse(product_id=old_product.id,
                                       product_name=old_product.name)  # Return правильный формат
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось обновить информацию о продукте",
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
        query = select(Wishlist).where(and_(Wishlist.user_id == user_data["user_id"], Wishlist.product_id == product_id))
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

    @classmethod
    async def add_in_cart(cls, request: Request, product_id: int, amount: float):
        user_data = await Functions.get_user_data(request)
        if amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Количество не может быть <= 0",
            )
        query = select(Product).where(Product.id == product_id)
        async with new_session() as db:
            result = await db.execute(query)
            result = result.scalars().first()
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Продукт не найден",
                )
            if result.amount < amount:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Количество превышает доступное значение",
                )
            field = Cart(user_id=user_data["user_id"], product_id=product_id, amount=amount)
            db.add(field)
            try:
                await db.commit()
                return {"message": "Продукт добавлен в корзину"}  # Правильный формат
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось добавить продукт в корзину, скорее всего он уже добавлен",
                )

    @classmethod
    async def change_product_amount_in_cart(cls, request: Request, product_id: int, amount: float):
        user_data = await Functions.get_user_data(request)
        if amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Количество не может быть <= 0",
            )
        query = select(Product).where(Product.id == product_id)
        async with new_session() as db:
            result = await db.execute(query)
            result = result.scalars().first()
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Продукт не найден",
                )
            if result.amount < amount:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Количество превышает доступное значение",
                )
            query = select(Cart).where(and_(Cart.user_id == user_data["user_id"], Cart.product_id == product_id))
            result = await db.execute(query)
            result = result.scalars().first()
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Продукт не найден в корзине",
                )
            result.amount = amount
            try:
                await db.commit()
                return {"message": "Корзина обновлена"}  # Правильный формат
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось обновить корзину",
                )

    @classmethod
    async def delete_from_cart(cls, request: Request, product_id: int):
        user_data = await Functions.get_user_data(request)
        query = select(Cart).where(
            and_(Cart.user_id == user_data["user_id"], Cart.product_id == product_id))
        async with new_session() as db:
            result = await db.execute(query)
            result = result.scalars().first()
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Продукт не найден в корзине",
                )
            await db.delete(result)
            try:
                await db.commit()
                return {"message": "Продукт убран из корзины"}  # Правильный формат
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось убрать продукт из корзины",
                )

    @classmethod
    async def place_order(cls, request: Request):
        user_data = await Functions.get_user_data(request)
        user_id = user_data["user_id"]
        total_amount = 0.0
        items_info = []

        async with new_session() as db:
            cart_items = await db.execute(select(Cart).where(Cart.user_id == user_id))
            cart_items = cart_items.scalars().all()

            if not cart_items:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Корзина пуста"
                )

            # Рассчитываем общую сумму заказа и обновляем количество товара
            for item in cart_items:
                product = await db.execute(
                    select(Product).options(joinedload(Product.article)).where(Product.id == item.product_id))
                product = product.scalars().first()

                if not product:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Продукт с ID {item.product_id} не найден"
                    )

                # Check if article is loaded
                if not product.article:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Не удалось загрузить статью для продукта с ID {item.product_id}"
                    )

                # Определяем цену товара (со скидкой или без)
                if product.new_price is not None:
                    price = product.new_price
                else:
                    price = product.article.price

                total_amount += price * item.amount
                items_info.append({"product_id": product.id, "quantity": item.amount})

                # Уменьшаем количество товара
                product.amount -= item.amount
                if product.amount < 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Недостаточное количество товара  {product.name}"
                    )

            # Создаем запись о заказе
            new_order = Order(user_id=user_id, total_amount=total_amount, items=json.dumps(items_info))
            db.add(new_order)
            await db.commit()
            await db.refresh(new_order)

            # Очищаем корзину пользователя
            for item in cart_items:
                await db.delete(item)
            await db.commit()

            return {"order_id": new_order.id, "total_amount": total_amount,
                    "message": "Заказ успешно создан, ожидается оплата"}


    @classmethod
    async def pay_order(cls, request: Request, order_id: int, pay: bool):
        user_data = await Functions.get_user_data(request)
        user_id = user_data["user_id"]

        async with new_session() as db:
            result = await db.execute(select(Order).where(Order.id == order_id))
            order = result.scalars().first()

            if not order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Заказ не найден"
                )

            # Проверяем, является ли текущий пользователь владельцем заказа
            if order.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Вы не можете оплатить этот заказ, так как он принадлежит другому пользователю."
                )

            if order.payment_status == "paid":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Этот заказ уже оплачен и не может быть изменен."
                )

            if order.payment_status == "failed":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Этот заказ был отменен и не может быть оплачен снова."
                )

            # Если pay == False - отменяем оплату
            if pay == False:
                # если платеж был отменен
                if order.payment_status == "failed":
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Вы уже отменили заказ"
                    )
                # Возвращаем количество товаров на склад
                items_info = json.loads(order.items)
                for item in items_info:
                    product_result = await db.execute(select(Product).where(Product.id == item["product_id"]))
                    product = product_result.scalars().first()
                    if not product:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Продукт с ID {item['product_id']} не найден"
                        )
                    product.amount += item["quantity"]

                order.payment_status = "failed"
                await db.commit()
                return {"message": "Оплата отменена, количество товаров возвращено на склад", "order_id": order.id}

            # Если pay == True - проводим оплату
            if pay == True:
                # Увеличиваем счетчик покупок для каждого товара в заказе
                items_info = json.loads(order.items)
                for item in items_info:
                    product_result = await db.execute(select(Product).where(Product.id == item["product_id"]))
                    product = product_result.scalars().first()
                    if not product:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Продукт с ID {item['product_id']} не найден"
                        )
                    product.purchase_count += item["quantity"]
                    await ProductService.check_product_hit(product)

                # Устанавливаем статус заказа как "оплачен"
                order.payment_status = "paid"
                await db.commit()

                return {"message": "Оплата успешно проведена", "order_id": order.id}

    @classmethod
    async def get_order_history(cls, request: Request):
        """
        Получает историю заказов пользователя.
        """
        user_data = await Functions.get_user_data(request)
        user_id = user_data["user_id"]

        async with new_session() as db:
            orders = await db.execute(select(Order).where(Order.user_id == user_id).order_by(Order.order_date.desc()))
            orders = orders.scalars().all()

            if not orders:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="История заказов пуста"
                )

            order_history = []
            for order in orders:
                order_history.append({
                    "order_id": order.id,
                    "order_date": order.order_date,
                    "total_amount": order.total_amount,
                    "payment_status": order.payment_status
                })

            return order_history

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
    async def check_product_hit(cls, product: Product):
        async with new_session() as db:
            if product.purchase_count >= 500 and not product.hit:
                product.hit = True
                product.last_hit_date = datetime.utcnow()
                product.purchase_count = 0
                await db.commit()
                print(f"Product {product.name} has become a hit!")

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
            cls, request: Request, product_id: int, is_promotion: bool, procent_promotion: float
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
                if procent_promotion is None or not 0 < procent_promotion <= 100:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Процент скидки должен быть указан в диапазоне от 1 до 100",
                    )

                article_field = await db.execute(
                    select(Article).where(Article.id == product.article_id)
                )
                article_field = article_field.scalars().first()
                if article_field is None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Такого артикула не существует",
                    )

                old_price = float(article_field.price)
                discount_amount = old_price * (procent_promotion / 100)
                new_price = old_price - discount_amount

                product.promotion = is_promotion
                product.procent_promotion = procent_promotion
                product.old_price = old_price
                product.new_price = new_price
            else:
                product.promotion = is_promotion
                product.procent_promotion = None
                product.old_price = None
                product.new_price = None

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
    async def get_new_products(cls):
        async with new_session() as db:
            query = select(Product).options(joinedload(Product.article)).where(Product.new == True)
            result = await db.execute(query)
            products = result.scalars().all()

            return [
                {
                    "product_id": p.id,
                    "article_id": p.article_id,
                    "product_name": p.name,
                    "product_amount": p.amount,
                    "article_description": p.article.description,
                    "country": p.article.country,
                    "characteristic_color": p.article.characteristic_color,
                    "characteristic_width": p.article.characteristic_width,
                    "characteristic_density": p.article.characteristic_density,
                    "characteristic_consist": p.article.characteristic_consist,
                    # "article_price": p.article.price,
                    # "hit": p.hit,
                    # "promotion": p.promotion,
                    # "procent_promotion": p.procent_promotion,
                    # "new": p.new,
                    # "old_price": p.old_price,
                    # "new_price": p.new_price,
                }
                for p in products
            ]

    @classmethod
    async def get_promotion_products(cls):
        async with new_session() as db:
            query = select(Product).options(joinedload(Product.article)).where(
                Product.promotion == True
            )
            result = await db.execute(query)
            products = result.scalars().all()

            return [
                {
                    "product_id": p.id,
                    "article_id": p.article_id,
                    "product_name": p.name,
                    # "product_amount": p.amount,
                    "article_description": p.article.description,
                    "country": p.article.country,
                    "characteristic_color": p.article.characteristic_color,
                    "characteristic_width": p.article.characteristic_width,
                    "characteristic_density": p.article.characteristic_density,
                    "characteristic_consist": p.article.characteristic_consist,
                    # "article_price": p.article.price,
                    # "hit": p.hit,
                     "promotion": p.promotion,
                    # "procent_promotion": p.procent_promotion,
                    # "new": p.new,
                    "old_price": p.old_price,
                    "new_price": p.new_price,
                }
                for p in products
            ]

    @classmethod
    async def get_hit_products(cls):
        async with new_session() as db:
            query = select(Product).options(joinedload(Product.article)).where(
                Product.hit == True
            )
            result = await db.execute(query)
            products = result.scalars().all()

            return [
                {
                    "product_id": p.id,
                    "article_id": p.article_id,
                    "product_name": p.name,
                    "product_amount": p.amount,
                    "article_description": p.article.description,
                    "country": p.article.country,
                    "characteristic_color": p.article.characteristic_color,
                    "characteristic_width": p.article.characteristic_width,
                    "characteristic_density": p.article.characteristic_density,
                    "characteristic_consist": p.article.characteristic_consist,
                    "hit": p.hit,
                    "promotion": p.promotion,
                    "new": p.new,
                }
                for p in products
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
