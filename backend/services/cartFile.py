import json
import os
from datetime import date, timedelta, datetime
from typing import Sequence
from fastapi import UploadFile, HTTPException, status, Request, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import joinedload, contains_eager
from database import *
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select, delete, Select, and_, or_
from schemas import *
from Function import Functions, SECRET_KEY, ALGORITHM
from uuid import uuid4
import shutil
import jwt


class CartService:
    @classmethod
    async def add_in_cart(cls, request: Request, product_id: int, amount: float, response: Response):
        try:
            user_data = await Functions.get_user_data(request)
        except HTTPException:
            return await CartService.add_in_cart_unauth(request, product_id, amount, response)
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

            query = select(Cart).where(and_(Cart.user_id == user_data["user_id"], Cart.product_id == product_id))
            cart_item = await db.execute(query)
            cart_item = cart_item.scalars().first()
            if cart_item is not None:
                temp_amount = cart_item.amount + amount
                if result.amount < temp_amount:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Количество превышает доступное значение (включая количество в корзине)",
                    )
                cart_item.amount = temp_amount
                try:
                    await db.commit()
                    return {"message": "Корзина обновлена"}  # Правильный формат
                except IntegrityError:
                    await db.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось обновить корзину",
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
                    detail="Не удалось добавить продукт в корзину",
                )

    @classmethod
    async def add_in_cart_for_auth_request(cls, user_id: int, product_id: int, amount: float):
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

            query = select(Cart).where(and_(Cart.user_id == user_id, Cart.product_id == product_id))
            cart_item = await db.execute(query)
            cart_item = cart_item.scalars().first()
            if cart_item is not None:
                temp_amount = cart_item.amount + amount
                if result.amount < temp_amount:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Количество превышает доступное значение (включая количество в корзине)",
                    )
                cart_item.amount = temp_amount
                try:
                    await db.commit()
                    return {"message": "Корзина обновлена"}  # Правильный формат
                except IntegrityError:
                    await db.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось обновить корзину",
                    )

            if result.amount < amount:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Количество превышает доступное значение",
                )

            field = Cart(user_id=user_id, product_id=product_id, amount=amount)
            db.add(field)
            try:
                await db.commit()
                return {"message": "Продукт добавлен в корзину"}  # Правильный формат
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось добавить продукт в корзину",
                )

    @classmethod
    async def add_in_cart_unauth(cls, request: Request, product_id: int, amount: float, response: Response):
        cookie_cart = request.cookies.get("cart")
        if cookie_cart is not None:
            try:
                payload: list[dict[str, int]] = jwt.decode(cookie_cart, SECRET_KEY, algorithms=[ALGORITHM])["cart"]
            except jwt.InvalidTokenError or jwt.ExpiredSignatureError:
                response.delete_cookie("cart")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Куки корзины устарели и были очищены",
                )
            data: list[CartInfo] = [CartInfo(**item) for item in payload]
        else:
            data: list[CartInfo] = []

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

        product_in_cart = False
        for cart_item in data:
            if cart_item.product_id == product_id:
                temp_amount = cart_item.amount + amount
                if result.amount < temp_amount:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Количество превышает доступное значение (включая количество в корзине)",
                    )
                cart_item.amount = temp_amount
                product_in_cart = True
                break
        if product_in_cart:
            cookie_data = jwt.encode({"cart": [elem.__dict__ for elem in data]}, SECRET_KEY, algorithm=ALGORITHM)
            response.set_cookie(key="cart", value=cookie_data, httponly=False, secure=False)
            return {"message": "Корзина обновлена"}

        if result.amount < amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Количество превышает доступное значение",
            )

        data.append(CartInfo(product_id=product_id, amount=amount))
        cookie_data = jwt.encode({"cart": [elem.__dict__ for elem in data]}, SECRET_KEY, algorithm=ALGORITHM)
        response.set_cookie(key="cart", value=cookie_data, httponly=False, secure=False)
        return {"message": "Продукт добавлен в корзину"}

    @classmethod
    async def get_user_cart(cls, request: Request, response: Response) -> CartResponse:
        try:
            user_data = await Functions.get_user_data(request)
        except HTTPException:
            return await CartService.get_user_cart_unauth(request, response)
        query = select(Cart).options(
            joinedload(Cart.product)).where(Cart.user_id == user_data["user_id"])
        async with new_session() as db:
            cart_items = await db.execute(query)
            user_query = select(Wishlist).where(Wishlist.user_id == user_data["user_id"])
            user_wishlist = await db.execute(user_query)
            user_wishlist = user_wishlist.scalars().all()
            user_wishlist_ids = [wishlist_elem.product_id for wishlist_elem in user_wishlist]
        cart_items = cart_items.scalars().all()

        items: List[CartItem] = []
        total_products_price: float = 0
        total_promotion_price: float = 0

        for cart_item in cart_items:
            if cart_item.amount > cart_item.product.amount:
                if cart_item.product.amount == 0:
                    async with new_session() as db:
                        await db.delete(cart_item)
                        await db.commit()
                    continue
                else:
                    async with new_session() as db:
                        cart_item.amount = cart_item.product.amount
                        await db.commit()
                    cart_amount = cart_item.product.amount
            else:
                cart_amount = cart_item.amount

            price = (cart_item.product.new_price if
                     cart_item.product.promotion and cart_item.product.new_price is not None
                     else cart_item.product.price)
            total_products_price += cart_amount * cart_item.product.price

            total_price = round(cart_amount * price, 2)
            if cart_item.product.new_price is not None:
                total_promotion_price += round(cart_amount * cart_item.product.price, 2) - total_price
            if cart_item.product_id in user_wishlist_ids:
                wishlist_state = True
            else:
                wishlist_state = False
            item = CartItem(
                product_id=cart_item.product_id,
                article_id=cart_item.product.article_id,
                product_name=cart_item.product.name,
                product_measured_in=cart_item.product.measured_in,
                product_amount=cart_item.product.amount,
                product_amount_in_cart=cart_amount,
                product_price=cart_item.product.price,
                product_percent_promotion=cart_item.product.percent_promotion,
                product_new_price=cart_item.product.new_price,
                total_price=total_price,
                product_in_wishlist=wishlist_state
            )
            items.append(item)
        total_products_price = round(total_products_price, 2)
        total_promotion_price = round(total_promotion_price, 2)
        total_cart_price = round(total_products_price - total_promotion_price, 2)
        return CartResponse(items=items, total_products_price=total_products_price,
                            total_promotion_price=total_promotion_price, total_cart_price=total_cart_price)

    @classmethod
    async def get_user_cart_unauth(cls, request: Request, response: Response) -> CartResponse:
        cookie_cart = request.cookies.get("cart")
        if cookie_cart is None:
            cookie_data = jwt.encode({"cart": []}, SECRET_KEY, algorithm=ALGORITHM)
            response.set_cookie(key="cart", value=cookie_data, httponly=False, secure=False)
            return CartResponse(items=[], total_products_price=0, total_promotion_price=0, total_cart_price=0)
        else:
            try:
                payload: list[dict[str, int]] = jwt.decode(cookie_cart, SECRET_KEY, algorithms=[ALGORITHM])["cart"]
            except jwt.InvalidTokenError or jwt.ExpiredSignatureError:
                response.delete_cookie("cart")
                return CartResponse(items=[], total_products_price=0, total_promotion_price=0, total_cart_price=0)
            data: list[CartInfo] = [CartInfo(**item) for item in payload]

        data = sorted(data, key=lambda x: x.product_id)
        data_ids = [elem.product_id for elem in data]
        query = select(Product).where(Product.id.in_(data_ids)).order_by(Product.id.asc())
        async with new_session() as db:
            cart_items = await db.execute(query)
        cart_items = cart_items.scalars().all()

        if len(cart_items) != len(data_ids):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Не все товары присутствуют в бд",
            )

        items: List[CartItem] = []
        total_products_price: float = 0
        total_promotion_price: float = 0

        index = 0
        cart_is_changed = False
        for cart_item in cart_items:
            if data[index].amount > cart_item.amount:
                cart_is_changed = True
                if cart_item.amount == 0:
                    data.pop(index)
                    continue
                else:
                    data[index].amount = cart_item.amount
                    cart_amount = cart_item.amount
            else:
                cart_amount = data[index].amount

            price = (cart_item.new_price if
                     cart_item.promotion and cart_item.new_price is not None
                     else cart_item.price)
            total_products_price += cart_amount * cart_item.price

            total_price = round(cart_amount * price, 2)
            if cart_item.new_price is not None:
                total_promotion_price += round(cart_amount * cart_item.price, 2) - total_price
            item = CartItem(
                product_id=cart_item.id,
                article_id=cart_item.article_id,
                product_name=cart_item.name,
                product_measured_in=cart_item.measured_in,
                product_amount=cart_item.amount,
                product_amount_in_cart=cart_amount,
                product_price=cart_item.price,
                product_percent_promotion=cart_item.percent_promotion,
                product_new_price=cart_item.new_price,
                total_price=total_price,
                product_in_wishlist=False
            )
            items.append(item)
            index += 1
        if cart_is_changed:
            cookie_data = jwt.encode({"cart": [elem.__dict__ for elem in data]}, SECRET_KEY, algorithm=ALGORITHM)
            response.set_cookie(key="cart", value=cookie_data, httponly=False, secure=False)
        total_products_price = round(total_products_price, 2)
        total_promotion_price = round(total_promotion_price, 2)
        total_cart_price = round(total_products_price - total_promotion_price, 2)
        return CartResponse(items=items, total_products_price=total_products_price,
                            total_promotion_price=total_promotion_price, total_cart_price=total_cart_price)

    @classmethod
    async def change_product_amount_in_cart(cls, request: Request, product_id: int, amount: float, response: Response):
        try:
            user_data = await Functions.get_user_data(request)
        except HTTPException:
            return await CartService.change_product_amount_in_cart_unauth(request, product_id, amount, response)
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
    async def change_product_amount_in_cart_unauth(cls, request: Request, product_id: int, amount: float, response: Response):
        cookie_cart = request.cookies.get("cart")
        if cookie_cart is not None:
            try:
                payload: list[dict[str, int]] = jwt.decode(cookie_cart, SECRET_KEY, algorithms=[ALGORITHM])["cart"]
            except jwt.InvalidTokenError or jwt.ExpiredSignatureError:
                response.delete_cookie("cart")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Куки корзины устарели и были очищены",
                )
            data: list[CartInfo] = [CartInfo(**item) for item in payload]
        else:
            data: list[CartInfo] = []

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

        product_in_cart = False
        for cart_item in data:
            if cart_item.product_id == product_id:
                if result.amount < amount:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Количество превышает доступное значение",
                    )
                cart_item.amount = amount
                product_in_cart = True
                break
        if product_in_cart is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Товара нет в корзине",
            )

        cookie_data = jwt.encode({"cart": [elem.__dict__ for elem in data]}, SECRET_KEY, algorithm=ALGORITHM)
        response.set_cookie(key="cart", value=cookie_data, httponly=False, secure=False)
        return {"message": "Количество обновлено"}

    @classmethod
    async def delete_from_cart(cls, request: Request, product_id: int, response: Response):
        try:
            user_data = await Functions.get_user_data(request)
        except HTTPException:
            return await CartService.delete_from_cart_unauth(request, product_id, response)
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
    async def delete_from_cart_unauth(cls, request: Request, product_id: int, response: Response):
        cookie_cart = request.cookies.get("cart")
        if cookie_cart is not None:
            try:
                payload: list[dict[str, int]] = jwt.decode(cookie_cart, SECRET_KEY, algorithms=[ALGORITHM])["cart"]
            except jwt.InvalidTokenError or jwt.ExpiredSignatureError:
                response.delete_cookie("cart")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Куки корзины устарели и были очищены",
                )
            data: list[CartInfo] = [CartInfo(**item) for item in payload]
        else:
            return {"message": "Корзина пуста"}

        item_to_remove = None
        for cart_item in data:
            if cart_item.product_id == product_id:
                item_to_remove = cart_item
        if item_to_remove is not None:
            data.remove(item_to_remove)
            cookie_data = jwt.encode({"cart": [elem.__dict__ for elem in data]}, SECRET_KEY, algorithm=ALGORITHM)
            response.set_cookie(key="cart", value=cookie_data, httponly=False, secure=False)
            return {"message": "Продукт убран из корзины"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Товара нет в корзине",
            )

    @classmethod
    async def clear_cart(cls, request: Request, response: Response):
        try:
            user_data = await Functions.get_user_data(request)
        except HTTPException:
            return await CartService.clear_cart_unauth(response)
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

    @classmethod
    async def clear_cart_unauth(cls, response: Response):
        cookie_data = jwt.encode({"cart": []}, SECRET_KEY, algorithm=ALGORITHM)
        response.set_cookie(key="cart", value=cookie_data, httponly=False, secure=False)
        return {"message": "Продукты убраны из корзины"}
