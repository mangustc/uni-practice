import os
from datetime import date, timedelta, datetime
from typing import Sequence
from fastapi import UploadFile, HTTPException, status, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import joinedload
from database import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete, Select
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
            "article_id": product_field.article_id,
            "product_name": product_field.name,
            "product_amount": product_field.amount,
            "article_description": product_field.article.description,
            "country": product_field.article.country,
            "characteristic_color": product_field.article.characteristic_color,
            "characteristic_width": product_field.article.characteristic_width,
            "characteristic_density": product_field.article.characteristic_density,
            "characteristic_consist": product_field.article.characteristic_consist,
            "article_price": product_field.article.price
        }  # Correct format

    @classmethod
    async def get_product_small_card(cls, product_id: int):
        query = select(Product).options(joinedload(Product.article)).where(Product.id == product_id)
        async with new_session() as db:
            result = await db.execute(query)
        product_field = result.scalars().first()
        if not product_field:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден"
            )
        return {
            "product_name": product_field.name,
            "article_price": product_field.article.price
        }  # Correct format

    @classmethod
    async def get_all_products(cls):
        query = select(Product).options(joinedload(Product.article))
        async with new_session() as db:
            result = await db.execute(query)
        products = result.scalars().all()
        return [
            {"article_id": p.article_id,
             "product_name": p.name,
             "product_amount": p.amount,
             "article_description": p.article.description,
             "country": p.article.country,
             "characteristic_color": p.article.characteristic_color,
             "characteristic_width": p.article.characteristic_width,
             "characteristic_density": p.article.characteristic_density,
             "characteristic_consist": p.article.characteristic_consist,
             "article_price": p.article.price} for p in products
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

            old_product.subcategory_id = data.article_id
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


    #Изменить логику согласно количество покупок!!!!!
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