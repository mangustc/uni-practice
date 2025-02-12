from typing import List
from sqlalchemy import select, asc, desc
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status

from database import Product, new_session, Article


class SortService:
    @classmethod
    async def sort_products_by_price_ascending(cls):
        async with new_session() as db:
            # Получаем продукты и article_id
            products = await db.execute(select(Product).options(joinedload(Product.article)))
            products = products.scalars().all()

            # Сортируем продукты на основе цены article
            products_sorted = sorted(products, key=lambda p: p.article.price if p.article else float('inf'))

            return [
                {"product_name": p.name, "price": p.article.price if p.article else None}
                for p in products_sorted
            ]

    @classmethod
    async def sort_products_by_price_descending(cls):
        async with new_session() as db:
            # Получаем продукты и article_id
            products = await db.execute(select(Product).options(joinedload(Product.article)))
            products = products.scalars().all()

            # Сортируем продукты на основе цены article
            products_sorted = sorted(products, key=lambda p: p.article.price if p.article else float('-inf'),
                                     reverse=True)

            return [
                {"product_name": p.name, "price": p.article.price if p.article else None}
                for p in products_sorted
            ]

    @classmethod
    async def sort_products_by_name_ascending(cls):
        async with new_session() as db:
            query = select(Product).options(joinedload(Product.article)).order_by(asc(Product.name))
            result = await db.execute(query)
            products = result.scalars().all()

            return [
                {"product_name": p.name, "amount": p.amount}
                for p in products
            ]

    @classmethod
    async def sort_products_by_name_descending(cls):
        async with new_session() as db:
            query = select(Product).options(joinedload(Product.article)).order_by(desc(Product.name))
            result = await db.execute(query)
            products = result.scalars().all()

            return [
                {"product_name": p.name, "amount": p.amount}
                for p in products
            ]
