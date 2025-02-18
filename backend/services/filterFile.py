import math
from typing import Optional, List
from sqlalchemy import select, and_, or_, asc, desc, func
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from schemas import *
from services import CategoryService
from database import Article, Product, new_session, Category, Characteristic, Color


class FilterService:
    @classmethod
    async def get_info_for_catalog_page(cls, category_id: int):
        query = select(Category).where(Category.id == category_id)
        async with new_session() as db:
            result = await db.execute(query)
        result = result.scalars().first()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Категория с таким id не найдена"
            )
        categories = await CategoryService.get_all_categories()

        category_ids = []
        temp_categories = [result]
        async with new_session() as db:
            while len(temp_categories) != 0:
                temp = [elem.id for elem in temp_categories]
                category_ids.extend(temp)
                query = select(Category).where(Category.parent_id.in_(temp))
                result = await db.execute(query)
                temp_categories = result.scalars().all()
            query = select(Product).options(
                joinedload(Product.characteristics)
                .joinedload(Characteristic.property),
                joinedload(Product.color)).where(Product.category_id.in_(category_ids))
            result = await db.execute(query)
        result = result.scalars().unique()
        number_of_products = 0
        properties = []
        colors = []
        products = []
        min_price = math.pow(10, 40)
        max_price = 0
        for elem in result:
            number_of_products += 1
            for characteristic in elem.characteristics:
                properties.append(
                    GetCharacteristicResponse(property_id=characteristic.property_id,
                                              property_name=characteristic.property.name,
                                              property_value=characteristic.property_value).__dict__)
            if elem.color_id is not None:
                colors.append(GetColorResponse(color_id=elem.color_id, color_name=elem.color.name).__dict__)
            if elem.price < min_price:
                min_price = elem.price
            if elem.price > max_price:
                max_price = elem.price
            products.append(
                ProductInCatalogInfo(product_id=elem.id, product_name=elem.name,
                                     product_measured_in=elem.measured_in, product_price=elem.price,
                                     product_new=elem.new, product_hit=elem.hit,
                                     product_promotion=elem.promotion,
                                     product_percent_promotion=elem.percent_promotion,
                                     product_new_price=elem.new_price)
            )
        temp_unique_properties = sorted([GetCharacteristicResponse(**dict(t))
                                         for t in {frozenset(d.items())for d in properties}],
                                        key=lambda x: x.property_id)
        unique_colors = sorted([GetColorResponse(**dict(t))
                                for t in {frozenset(d.items()) for d in colors}],
                               key=lambda x: x.color_name)
        unique_properties = []
        for elem in temp_unique_properties:
            flag = True
            for unique_property in unique_properties:
                if elem.property_id == unique_property.property_id:
                    unique_property.values.append(elem.property_value)
                    flag = False
                    break
            if flag:
                unique_properties.append(PropertyFilter(property_id=elem.property_id,
                                                        property_name=elem.property_name,
                                                        values=[elem.property_value]))
        for unique_property in unique_properties:
            unique_property.values = sorted(unique_property.values)
        return CatalogPageInfo(number_of_products=number_of_products, categories=categories,
                               min_price=min_price, max_price=max_price,
                               colors=unique_colors, properties=unique_properties, products=products)

    @classmethod
    async def get_products_by_category_name_true(cls, category_name: str, filters: dict = None,
                                            sort_by: str = None, filter_by_params: str = None):
        # Получаем категорию по имени
        query = select(Category).where(Category.name == category_name)
        async with new_session() as db:
            result = await db.execute(query)
        result = result.scalars().first()

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Категория с таким названием не найдена"
            )

        # Получаем все подкатегории и саму категорию
        category_ids = [result.id]
        categories = [result]

        while categories:
            temp = [elem.id for elem in categories]
            query = select(Category).where(Category.parent_id.in_(temp))
            async with new_session() as db:
                result = await db.execute(query)
            categories = result.scalars().all()
            category_ids.extend([cat.id for cat in categories])

        # Формируем базовый запрос на получение продуктов
        query = select(Product).options(
            joinedload(Product.category),
            joinedload(Product.color),
            joinedload(Product.characteristics)
        ).where(Product.category_id.in_(category_ids))

        # Применяем фильтры, если они заданы
        if filters:
            # Создаем подзапрос для фильтрации характеристик
            characteristic_filters = []

            for property_id, value in filters.items():
                characteristic_filters.append(
                    and_(
                        Characteristic.product_id == Product.id,
                        Characteristic.property_id == property_id,
                        Characteristic.property_value == value
                    )
                )

            # Используем GROUP BY и HAVING для фильтрации по всем характеристикам
            if characteristic_filters:
                subquery = (
                    select(Characteristic.product_id)
                    .filter(or_(*characteristic_filters))
                    .group_by(Characteristic.product_id)
                    .having(func.count(Characteristic.product_id) == len(filters))
                ).subquery()

                query = query.filter(Product.id.in_(subquery))

        # Добавляем условие для фильтрации по параметрам (hit, promotion, new)
        if filter_by_params:
            if filter_by_params == 'new':
                query = query.filter(Product.new.is_(True))
            elif filter_by_params == 'hit':
                query = query.filter(Product.hit.is_(True))
            elif filter_by_params == 'promotion':
                query = query.filter(Product.promotion.is_(True))

        # Применяем сортировку, если она задана
        if sort_by:
            sort_direction = 'asc'  # По умолчанию - по возрастанию
            if sort_by.startswith('-'):
                sort_direction = 'desc'
                sort_by = sort_by[1:]  # Убираем символ '-'

            if sort_by == "price":
                if sort_direction == 'asc':
                    query = query.order_by(asc(Product.price))
                else:
                    query = query.order_by(desc(Product.price))
            elif sort_by == "name":
                if sort_direction == 'asc':
                    query = query.order_by(asc(Product.name))
                else:
                    query = query.order_by(desc(Product.name))

        async with new_session() as db:
            result = await db.execute(query)

        products = result.scalars().unique().all()

        return [GetProductResponseWithNames(
            product_id=p.id,
            category_id=p.category_id,
            category_name=p.category.name,
            article_id=p.article_id,
            color_id=p.color_id,
            color_name=p.color.name if p.color else None,
            product_name=p.name,
            product_description=p.description,
            product_measured_in=p.measured_in,
            product_amount=p.amount,
            product_price=p.price,
            product_new=p.new,
            product_hit=p.hit,
            product_promotion=p.promotion,
            product_percent_promotion=p.percent_promotion,
            product_new_price=p.new_price
        ).__dict__ for p in products]

    @classmethod
    async def get_products_by_category_name_test(cls, category_name: str, filters: dict = None,
                                                 sort_by: str = None, filter_by_params: str = None):
        # Получаем категорию по имени
        query = select(Category).where(Category.name == category_name)
        async with new_session() as db:
            result = await db.execute(query)
        result = result.scalars().first()

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Категория с таким названием не найдена"
            )

        # Получаем все подкатегории и саму категорию
        category_ids = [result.id]
        categories = [result]

        while categories:
            temp = [elem.id for elem in categories]
            query = select(Category).where(Category.parent_id.in_(temp))
            async with new_session() as db:
                result = await db.execute(query)
            categories = result.scalars().all()
            category_ids.extend([cat.id for cat in categories])

        # Формируем базовый запрос на получение продуктов
        query = select(Product).options(
            joinedload(Product.category),
            joinedload(Product.color),
            joinedload(Product.characteristics)
        ).where(Product.category_id.in_(category_ids))

        # Применяем фильтры, если они заданы
        if filters:
            # Извлекаем color_name из фильтров
            color_name = filters.pop('color_name', None)  # Извлекаем color_name из фильтров

            if color_name:
                # Добавляем условие для фильтрации по цвету
                query = query.join(Color, Product.color_id == Color.id).filter(Color.name == color_name)

            # Создаем подзапрос для фильтрации характеристик
            characteristic_filters = []

            for property_id, value in filters.items():
                characteristic_filters.append(
                    and_(
                        Characteristic.product_id == Product.id,
                        Characteristic.property_id == property_id,
                        Characteristic.property_value == value
                    )
                )

            # Используем GROUP BY и HAVING для фильтрации по всем характеристикам
            if characteristic_filters:
                subquery = (
                    select(Characteristic.product_id)
                    .filter(or_(*characteristic_filters))
                    .group_by(Characteristic.product_id)
                    .having(func.count(Characteristic.product_id) == len(filters))
                ).subquery()

                query = query.filter(Product.id.in_(subquery))

        # Добавляем условие для фильтрации по параметрам (hit, promotion, new)
        if filter_by_params:
            if filter_by_params == 'new':
                query = query.filter(Product.new.is_(True))
            elif filter_by_params == 'hit':
                query = query.filter(Product.hit.is_(True))
            elif filter_by_params == 'promotion':
                query = query.filter(Product.promotion.is_(True))

        # Применяем сортировку, если она задана
        if sort_by:
            sort_direction = 'asc'  # По умолчанию - по возрастанию
            if sort_by.startswith('-'):
                sort_direction = 'desc'
                sort_by = sort_by[1:]  # Убираем символ '-'

            if sort_by == "price":
                if sort_direction == 'asc':
                    query = query.order_by(asc(Product.price))
                else:
                    query = query.order_by(desc(Product.price))
            elif sort_by == "name":
                if sort_direction == 'asc':
                    query = query.order_by(asc(Product.name))
                else:
                    query = query.order_by(desc(Product.name))

        async with new_session() as db:
            result = await db.execute(query)

        products = result.scalars().unique().all()

        return [GetProductResponseWithNames(
            product_id=p.id,
            category_id=p.category_id,
            category_name=p.category.name,
            article_id=p.article_id,
            color_id=p.color_id,
            color_name=p.color.name if p.color else None,
            product_name=p.name,
            product_description=p.description,
            product_measured_in=p.measured_in,
            product_amount=p.amount,
            product_price=p.price,
            product_new=p.new,
            product_hit=p.hit,
            product_promotion=p.promotion,
            product_percent_promotion=p.percent_promotion,
            product_new_price=p.new_price
        ).__dict__ for p in products]

    @classmethod
    async def search_products_by_name(cls, search_term: str, sort_by: str = None):
        """
        Поиск товаров по названию с возможностью сортировки.
        """

        # Формируем базовый запрос на получение продуктов
        query = select(Product).options(
            joinedload(Product.category),
            joinedload(Product.color)
        ).where(Product.name.ilike(f"%{search_term}%"))  # ilike for case-insensitive search

        # Применяем сортировку, если она задана
        if sort_by:
            sort_direction = 'asc'  # По умолчанию - по возрастанию
            if sort_by.startswith('-'):
                sort_direction = 'desc'
                sort_by = sort_by[1:]  # Убираем символ '-'

            if sort_by == "price":
                if sort_direction == 'asc':
                    query = query.order_by(asc(Product.price))
                else:
                    query = query.order_by(desc(Product.price))
            elif sort_by == "name":
                if sort_direction == 'asc':
                    query = query.order_by(asc(Product.name))
                else:
                    query = query.order_by(desc(Product.name))
            elif sort_by in ("hit", "new", "promotion"):  # Sorting by boolean fields
                if sort_direction == 'asc':
                    query = query.order_by(asc(getattr(Product, sort_by)))
                else:
                    query = query.order_by(desc(getattr(Product, sort_by)))

        async with new_session() as db:
            result = await db.execute(query)
            products = result.scalars().unique().all()

        return [GetProductResponseWithNames(
            product_id=p.id,
            category_id=p.category_id,
            category_name=p.category.name,
            article_id=p.article_id,
            color_id=p.color_id,
            color_name=p.color.name if p.color else None,
            product_name=p.name,
            product_description=p.description,
            product_measured_in=p.measured_in,
            product_amount=p.amount,
            product_price=p.price,
            product_new=p.new,
            product_hit=p.hit,
            product_promotion=p.promotion,
            product_percent_promotion=p.percent_promotion,
            product_new_price=p.new_price
        ).__dict__ for p in products]
