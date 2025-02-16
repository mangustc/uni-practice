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


class CartService:
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
    async def get_user_cart(cls, request: Request) -> CartResponse:
        user_data = await Functions.get_user_data(request)
        async with new_session() as db:
            query = select(Cart).where(Cart.user_id == user_data["user_id"])
            cart_items = await db.execute(query)
            cart_items = cart_items.scalars().all()

            items: List[CartItem] = []
            total_cart_price: float = 0.0

            for cart_item in cart_items:
                product_query = select(Product).where(Product.id == cart_item.product_id)
                product_result = await db.execute(product_query)
                product = product_result.scalars().first()

                if product:
                    article_query = select(Article).where(Article.id == product.article_id)
                    article_result = await db.execute(article_query)
                    article = article_result.scalars().first()

                    if article:
                        price = product.new_price if product.promotion and product.new_price is not None else article.price

                        total_price = cart_item.amount * price

                        item = CartItem(
                            product_id=cart_item.product_id,
                            product_name=product.name,
                            amount=cart_item.amount,
                            total_price=total_price,
                        )
                        items.append(item)
                        total_cart_price += total_price
                    else:
                        await db.delete(cart_item)
                        await db.commit()
                else:
                    await db.delete(cart_item)
                    await db.commit()

            return CartResponse(items=items, total_cart_price=total_cart_price)

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
