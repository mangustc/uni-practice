from typing import Optional, List
from sqlalchemy import select, and_
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status

from database import Article, Product, new_session


class FilterService:
    @classmethod
    async def filter_products(
        cls,
        price_min: Optional[int] = None,
        price_max: Optional[int] = None,
        countries: Optional[List[str]] = None,
        colors: Optional[List[str]] = None,
        widths: Optional[List[str]] = None,
        densities: Optional[List[str]] = None,
        consists: Optional[List[str]] = None,
    ):
        async with new_session() as db:
            query = select(Product).options(joinedload(Product.article))

            conditions = []

            if price_min is not None:
                conditions.append(Article.price >= price_min)
            if price_max is not None:
                conditions.append(Article.price <= price_max)
            if countries is not None and len(countries) > 0:
                conditions.append(Article.country.in_(countries))
            if colors is not None and len(colors) > 0:
                conditions.append(Article.characteristic_color.in_(colors))
            if widths is not None and len(widths) > 0:
                conditions.append(Article.characteristic_width.in_(widths))
            if densities is not None and len(densities) > 0:
                conditions.append(Article.characteristic_density.in_(densities))
            if consists is not None and len(consists) > 0:
                conditions.append(Article.characteristic_consist.in_(consists))

            if conditions:
                query = query.join(Article, Article.id == Product.article_id).where(and_(*conditions))

            result = await db.execute(query)
            products = result.scalars().all()

            return [
                {
                    "product_id": p.id,  # Add product_id
                    "article_id": p.article_id,
                    "product_name": p.name,
                    "product_amount": p.amount,
                    "article_description": p.article.description,
                    "country": p.article.country,
                    "characteristic_color": p.article.characteristic_color,
                    "characteristic_width": p.article.characteristic_width,
                    "characteristic_density": p.article.characteristic_density,
                    "characteristic_consist": p.article.characteristic_consist,
                    "article_price": p.article.price,
                }
                for p in products
            ]