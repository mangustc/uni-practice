import os
from datetime import date
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

            new_product = Product(article_id=data.article_id, name=data.name, amount=data.amount)
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
            "article_characteristics": product_field.article.characteristics,
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
             "article_characteristics": p.article.characteristics,
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