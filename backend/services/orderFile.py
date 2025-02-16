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


class OrderService:
    @classmethod
    async def place_order(cls, request: Request, order_request: PlaceOrderRequest):
        user_data = await Functions.get_user_data(request)
        user_id = user_data["user_id"]
        total_amount = 0.0
        items_info = []

        async with new_session() as db:
            # 1. Получаем товары из корзины
            cart_items_list = await db.execute(select(Cart).where(Cart.user_id == user_id))
            cart_items = cart_items_list.scalars().all()

            if not cart_items:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Корзина пуста"
                )

            # 2. Рассчитываем общую сумму заказа и обновляем количество товара
            for item in cart_items:
                product_result = await db.execute(
                    select(Product).where(Product.id == item.product_id)
                )
                product = product_result.scalars().first()

                if not product:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Продукт с ID {item.product_id} не найден"
                    )

                # Определяем цену товара (со скидкой или без)
                if product.new_price is not None:
                    price = product.new_price
                else:
                    price = product.price

                total_amount += price * item.amount
                items_info.append({"product_id": product.id, "quantity": item.amount})

                # Уменьшаем количество товара
                product.amount -= item.amount
                if product.amount < 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Недостаточное количество товара  {product.name}"
                    )

            # 3. Получаем службу доставки
            delivery_service_result = await db.execute(
                select(DeliveryService).where(DeliveryService.id == order_request.delivery_service_id)
            )
            delivery_service = delivery_service_result.scalars().first()

            if not delivery_service:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Служба доставки не найдена"
                )

            total_amount += delivery_service.price  # Add delivery price to total

            # 4. Создаем запись о заказе
            new_order = Order(
                user_id=user_id,
                total_amount=total_amount,
                items=json.dumps(items_info),
                delivery_service=delivery_service  # Assign the delivery service
            )
            db.add(new_order)
            await db.commit()
            await db.refresh(new_order)

            for cart_item in cart_items:
                await db.delete(cart_item)
            await db.commit()

            return {"order_id": new_order.id, "total_amount": total_amount,
                    "message": "Заказ успешно создан, ожидается оплата"}

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
    async def check_product_hit(cls, product: Product):
        async with new_session() as db:
            if product.purchase_count >= 500 and not product.hit:
                product.hit = True
                product.last_hit_date = datetime.utcnow()
                product.purchase_count = 0
                await db.commit()
                print(f"Product {product.name} has become a hit!")

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
                    await OrderService.check_product_hit(product)

                # Устанавливаем статус заказа как "оплачен"
                order.payment_status = "paid"
                await db.commit()

                return {"message": "Оплата успешно проведена", "order_id": order.id}