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
        query = select(Cart).options(
            joinedload(Cart.product)).where(Cart.user_id == user_data["user_id"])
        async with new_session() as db:
            cart_items = await db.execute(query)
        cart_items = cart_items.scalars().all()

        items: List[CartItem] = []
        total_products_price: float = 0
        total_promotion_price: float = 0

        for cart_item in cart_items:
            price = (cart_item.product.new_price if
                     cart_item.product.promotion and cart_item.product.new_price is not None
                     else cart_item.product.price)
            total_products_price += cart_item.amount * cart_item.product.price

            total_price = round(cart_item.amount * price, 2)
            if cart_item.product.new_price is not None:
                total_promotion_price += round(cart_item.amount * cart_item.product.price, 2) - total_price

            item = CartItem(
                product_id=cart_item.product_id,
                article_id=cart_item.product.article_id,
                product_name=cart_item.product.name,
                product_measured_in=cart_item.product.measured_in,
                product_amount=cart_item.product.amount,
                product_amount_in_cart=cart_item.amount,
                product_price=cart_item.product.price,
                product_percent_promotion=cart_item.product.percent_promotion,
                product_new_price=cart_item.product.new_price,
                total_price=total_price
            )
            items.append(item)
        total_products_price = round(total_products_price, 2)
        total_promotion_price = round(total_promotion_price, 2)
        total_cart_price = round(total_products_price - total_promotion_price, 2)
        return CartResponse(items=items, total_products_price=total_products_price,
                            total_promotion_price=total_promotion_price, total_cart_price=total_cart_price)

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
    async def clear_cart(cls, request: Request):
        user_data = await Functions.get_user_data(request)
        query = delete(Cart).where(Cart.user_id == user_data["user_id"])
        async with new_session() as db:
            result = await db.execute(query)
            try:
                await db.commit()
                return {"message": "Продукты убраны из корзины"}  # Правильный формат
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось убрать продукты из корзины",
                )