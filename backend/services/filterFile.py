from typing import Optional, List
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from database import Article, new_session


# class FilterService:
#     @classmethod
#     async def filter_articles(cls, price_min: Optional[int] = None, price_max: Optional[int] = None,
#     countries: Optional[List[str]] = None, colors: Optional[List[str]] = None,):
#         async with new_session() as db:
#             query = select(Article)
#
#             conditions = []
#
#             if price_min is not None:
#                 conditions.append(Article.price >= price_min)
#             if price_max is not None:
#                 conditions.append(Article.price <= price_max)
#             if countries is not None and len(countries) > 0:
#                 conditions.append(Article.country.in_(countries))
#             if colors is not None and len(colors) > 0:
#                 conditions.append(Article.characteristic_color.in_(colors))
#
#             if conditions:
#                 query = query.where(and_(*conditions))
#
#             result = await db.execute(query)
#             articles = result.scalars().all()
#
#             return [
#                 {
#                     "subcategory_id": a.subcategory_id,
#                     "description": a.description,
#                     "country": a.country,
#                     "price": a.price,
#                     "characteristic_color": a.characteristic_color,
#                     "characteristic_width": a.characteristic_width,
#                     "characteristic_density": a.characteristic_density,
#                     "characteristic_consist": a.characteristic_consist,
#                 }
#                 for a in articles
#             ]


class FilterService:
    @classmethod
    async def filter_articles(
        cls,
        price_min: Optional[int] = None,
        price_max: Optional[int] = None,
        countries: Optional[List[str]] = None,
        colors: Optional[List[str]] = None,
        widths: Optional[List[str]] = None,
        densities: Optional[List[str]] = None,
        consists: Optional[List[str]] = None,
    ):
        """
        Filters articles based on price range, countries, colors, widths, densities, and consists.
        All parameters are optional and can be combined.
        """
        async with new_session() as db:
            query = select(Article)

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
                query = query.where(and_(*conditions))

            result = await db.execute(query)
            articles = result.scalars().all()

            return [
                {
                    "subcategory_id": a.subcategory_id,
                    "description": a.description,
                    "country": a.country,
                    "price": a.price,
                    "characteristic_color": a.characteristic_color,
                    "characteristic_width": a.characteristic_width,
                    "characteristic_density": a.characteristic_density,
                    "characteristic_consist": a.characteristic_consist,
                }
                for a in articles
            ]