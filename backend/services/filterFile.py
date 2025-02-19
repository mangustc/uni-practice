import math
from typing import Optional, List
from sqlalchemy import select, and_, or_, asc, desc, func, case
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
                                        key=lambda x: x.property_name)
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
                unique_properties.append(PropertyFilter1(property_id=elem.property_id,
                                                        property_name=elem.property_name,
                                                        values=[elem.property_value]))
        for unique_property in unique_properties:
            unique_property.values = sorted(unique_property.values)
        return CatalogPageInfo(number_of_products=number_of_products, categories=categories,
                               min_price=min_price, max_price=max_price,
                               colors=unique_colors, properties=unique_properties, products=products)
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

    @classmethod
    async def get_products_by_category_id(
            cls,
            filters: CatalogFilters,
            sort_by: SortByEnum,
            filter_by_params: FilterByParamsEnum
    ):
        """
        Получает продукты по ID категории с применением фильтров и сортировки.
        """

        # Получаем все подкатегории и саму категорию
        category_ids = await cls.get_all_subcategory_ids(filters.categoryID)

        # Определяем цену для фильтрации в зависимости от акции
        price_to_filter = case(
            (Product.promotion == True, Product.new_price),
            else_=Product.price
        ).label("price_to_filter")

        # Формируем базовый запрос на получение продуктов
        query = select(Product).options(
            joinedload(Product.category),
            joinedload(Product.color),
            joinedload(Product.characteristics)
        ).where(Product.category_id.in_(category_ids))

        # Применяем фильтры из объекта filters
        if filters:
            if filters.productOnlyInStock:
                query = query.filter(Product.amount > 0)
            elif filters.productOnlyInStock is False:
                query = query.filter(Product.amount == 0)

            if filters.productPriceStart is not None:
                query = query.filter(price_to_filter >= filters.productPriceStart)

            if filters.productPriceEnd is not None:
                query = query.filter(price_to_filter <= filters.productPriceEnd)

            if filters.colors:
                query = query.filter(Product.color_id.in_(filters.colors))

            if filters.properties:
                characteristic_filters = []
                for prop_filter in filters.properties:
                    characteristic_filters.append(
                        and_(
                            Characteristic.product_id == Product.id,
                            Characteristic.property_id == prop_filter.propertyID,
                            Characteristic.property_value.in_(prop_filter.propertyValues)
                        )
                    )

                if characteristic_filters:
                    subquery = (
                        select(Characteristic.product_id)
                        .filter(or_(*characteristic_filters))
                        .group_by(Characteristic.product_id)
                        .having(func.count(Characteristic.product_id) == len(filters.properties))
                    ).subquery()

                    #query = query.filter(Product.id.in_(subquery))
                    query = query.filter(Product.id.in_(select(subquery.c.product_id)))

        # Добавляем условие для фильтрации по параметрам (hit, promotion, new)
        if filter_by_params:
            if filter_by_params == FilterByParamsEnum.new:
                query = query.filter(Product.new.is_(True))
            elif filter_by_params == FilterByParamsEnum.hit:
                query = query.filter(Product.hit.is_(True))
            elif filter_by_params == FilterByParamsEnum.promotion:
                query = query.filter(Product.promotion.is_(True))

        # Применяем сортировку
        if sort_by == SortByEnum.price_asc:
            query = query.order_by(asc(Product.price))
        elif sort_by == SortByEnum.price_desc:
            query = query.order_by(desc(Product.price))
        elif sort_by == SortByEnum.name_asc:
            query = query.order_by(asc(Product.name))
        elif sort_by == SortByEnum.name_desc:
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
    async def get_all_subcategory_ids(cls, category_id: int) -> List[int]:
        """
        Рекурсивно получает все ID подкатегорий для заданной категории.
        """
        category_ids = [category_id]
        categories_to_check = [category_id]

        async with new_session() as db:
            while categories_to_check:
                parent_id = categories_to_check.pop(0)
                query = select(Category.id).where(Category.parent_id == parent_id)
                result = await db.execute(query)
                sub_ids = [row[0] for row in result.all()]
                category_ids.extend(sub_ids)
                categories_to_check.extend(sub_ids)
        return category_ids
