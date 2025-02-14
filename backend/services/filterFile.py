from typing import Optional, List
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from schemas import *
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
                # Учитываем акционную цену, если она есть
                price_condition = []
                price_condition.append(
                    and_(
                        Product.promotion == False, Article.price >= price_min
                    )
                )
                price_condition.append(
                    and_(
                        Product.promotion == True, Product.new_price >= price_min
                    )
                )
                conditions.append(or_(*price_condition))

            if price_max is not None:
                # Учитываем акционную цену, если она есть
                price_condition = []
                price_condition.append(
                    and_(
                        Product.promotion == False, Article.price <= price_max
                    )
                )
                price_condition.append(
                    and_(
                        Product.promotion == True, Product.new_price <= price_max
                    )
                )
                conditions.append(or_(*price_condition))

            if countries is not None and len(countries) > 0:
                conditions.append(Article.country.in_(countries))
            if colors is not None and len(colors) > 0:
                conditions.append(Product.characteristic_color.in_(colors))
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

            product_list = [
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

            return product_list