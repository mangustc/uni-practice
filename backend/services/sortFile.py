from typing import List
from sqlalchemy import select, asc, desc
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from schemas import *

from database import Product, new_session, Article


class SortService:
    @classmethod
    async def sort_products_by_price_ascending(cls):
        async with new_session() as db:
            products = await db.execute(select(Product).options(joinedload(Product.article)))
            products = products.scalars().all()

            products_sorted = sorted(products, key=lambda p: p.new_price if p.promotion and p.new_price is not None else p.article.price)

            return [
                GetProductResponse(
                    product_id=p.id,
                    article_id=p.article_id,
                    product_name=p.name,
                    product_amount=p.amount,
                    article_description=p.article.description,
                    article_country=p.article.country,
                    product_characteristic_color=p.characteristic_color,
                    article_characteristic_width=p.article.characteristic_width,
                    article_characteristic_density=p.article.characteristic_density,
                    article_characteristic_consist=p.article.characteristic_consist,
                    article_measured_in=p.article.measured_in,
                    article_price=p.article.price,
                    product_new=p.new,
                    product_hit=p.hit,
                    product_promotion=p.promotion,
                    product_percent_promotion=int(p.percent_promotion) if p.percent_promotion else None,
                    product_new_price=p.new_price,
                ).__dict__
                for p in products_sorted
            ]

    @classmethod
    async def sort_products_by_price_descending(cls):
        async with new_session() as db:
            products = await db.execute(select(Product).options(joinedload(Product.article)))
            products = products.scalars().all()
            products_sorted = sorted(products, key=lambda p: p.new_price if p.promotion and p.new_price is not None else p.article.price, reverse=True)

            return [
                GetProductResponse(
                    product_id=p.id,
                    article_id=p.article_id,
                    product_name=p.name,
                    product_amount=p.amount,
                    article_description=p.article.description,
                    article_country=p.article.country,
                    product_characteristic_color=p.characteristic_color,
                    article_characteristic_width=p.article.characteristic_width,
                    article_characteristic_density=p.article.characteristic_density,
                    article_characteristic_consist=p.article.characteristic_consist,
                    article_measured_in=p.article.measured_in,
                    article_price=p.article.price,
                    product_new=p.new,
                    product_hit=p.hit,
                    product_promotion=p.promotion,
                    product_percent_promotion=int(p.percent_promotion) if p.percent_promotion else None,
                    product_new_price=p.new_price,
                ).__dict__
                for p in products_sorted
            ]

    @classmethod
    async def sort_products_by_name_ascending(cls):
        async with new_session() as db:
            query = select(Product).options(joinedload(Product.article)).order_by(asc(Product.name))
            result = await db.execute(query)
            products = result.scalars().all()

            return [
                GetProductResponse(
                    product_id=p.id,
                    article_id=p.article_id,
                    product_name=p.name,
                    product_amount=p.amount,
                    article_description=p.article.description,
                    article_country=p.article.country,
                    product_characteristic_color=p.characteristic_color,
                    article_characteristic_width=p.article.characteristic_width,
                    article_characteristic_density=p.article.characteristic_density,
                    article_characteristic_consist=p.article.characteristic_consist,
                    article_measured_in=p.article.measured_in,
                    article_price=p.article.price,
                    product_new=p.new,
                    product_hit=p.hit,
                    product_promotion=p.promotion,
                    product_percent_promotion=int(p.percent_promotion) if p.percent_promotion else None,
                    product_new_price=p.new_price,
                ).__dict__
                for p in products
            ]

    @classmethod
    async def sort_products_by_name_descending(cls):
        async with new_session() as db:
            query = select(Product).options(joinedload(Product.article)).order_by(desc(Product.name))
            result = await db.execute(query)
            products = result.scalars().all()

            return [
                GetProductResponse(
                    product_id=p.id,
                    article_id=p.article_id,
                    product_name=p.name,
                    product_amount=p.amount,
                    article_description=p.article.description,
                    article_country=p.article.country,
                    product_characteristic_color=p.characteristic_color,
                    article_characteristic_width=p.article.characteristic_width,
                    article_characteristic_density=p.article.characteristic_density,
                    article_characteristic_consist=p.article.characteristic_consist,
                    article_measured_in=p.article.measured_in,
                    article_price=p.article.price,
                    product_new=p.new,
                    product_hit=p.hit,
                    product_promotion=p.promotion,
                    product_percent_promotion=int(p.percent_promotion) if p.percent_promotion else None,
                    product_new_price=p.new_price,
                ).__dict__
                for p in products
            ]