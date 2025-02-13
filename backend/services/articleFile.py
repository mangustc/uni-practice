import os
from datetime import date
from typing import Sequence
from fastapi import UploadFile, HTTPException, status, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import joinedload
from database import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete, Select
from schemas import *
from Function import Functions
from uuid import uuid4
import shutil


class ArticleService:
    @classmethod
    async def create_article(cls, request: Request, data: CreateArticle):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут добавлять категории"
            )

        async with new_session() as db:
            category = await db.execute(
                select(Category).where(Category.name == data.category_name)
            )
            category = category.scalars().first()
            if category is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Категории с таким именем не существует",
                )

            new_article = Article(
                category_id=category.id,
                description=data.description,
                country=data.country,
                measured_in=data.measured_in,
                price=data.price,
                characteristic_width=None,
                characteristic_density=None,
                characteristic_consist=None,
            )
            db.add(new_article)
            try:
                await db.commit()
                await db.refresh(new_article)
                return ArticleResponse(article_id=new_article.id)
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось добавить артикул",
                )

    @classmethod
    async def get_article(cls, article_id: int):
        query = select(Article).where(Article.id == article_id)
        async with new_session() as db:
            result = await db.execute(query)
        article = result.scalars().first()
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден"
            )
        return {
            "article_category_id": article.category_id,
            "article_description": article.description,
            "article_country": article.country,
            "article_measured_in": article.measured_in,
            "article_price": article.price,
            "article_characteristic_width": article.characteristic_width,
            "article_characteristic_density": article.characteristic_density,
            "article_characteristic_consist": article.characteristic_consist,
        }

    @classmethod
    async def get_all_articles(cls):
        query = select(Article)
        async with new_session() as db:
            result = await db.execute(query)
        articles = result.scalars().all()
        return [
            {
                "article_category_id": a.category_id,
                "article_description": a.description,
                "article_country": a.country,
                "article_measured_in": a.measured_in,
                "article_price": a.price,
                "article_characteristic_width": a.characteristic_width,
                "article_characteristic_density": a.characteristic_density,
                "article_characteristic_consist": a.characteristic_consist,
            } for a in articles
        ]

    @classmethod
    async def update_article_information(cls, request: Request, article_id: int, data: CreateArticle):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут обновлять информацию об артикуле"
            )

        async with new_session() as db:
            old_article = await db.execute(select(Article).where(Article.id == article_id))
            old_article = old_article.scalars().first()
            if old_article is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Такого артикула не существует",
                )

            category = await db.execute(
                select(Category).where(Category.name == data.category_name)
            )
            category = category.scalars().first()
            if category is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Подкатегории с таким именем не существует",
                )

            old_article.category_id = category.id
            old_article.description = data.description
            old_article.country = data.country
            old_article.measured_in = data.measured_in
            old_article.price = data.price

            try:
                await db.commit()
                await db.refresh(old_article)
                return ArticleResponse(article_id=old_article.id)
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось обновить информацию об артикуле",
                )

    @classmethod
    async def update_article_characteristics(cls, request: Request, article_id: int, data: UpdateArticleCharacteristics):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут обновлять характеристики артикула"
            )

        async with new_session() as db:
            old_article = await db.execute(select(Article).where(Article.id == article_id))
            old_article = old_article.scalars().first()

            if old_article is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Такого артикула не существует",
                )

            if data.characteristic_width is not None:
                old_article.characteristic_width = data.characteristic_width
            if data.characteristic_density is not None:
                old_article.characteristic_density = data.characteristic_density
            if data.characteristic_consist is not None:
                old_article.characteristic_consist = data.characteristic_consist

            try:
                await db.commit()
                await db.refresh(old_article)
                return ArticleResponse(article_id=old_article.id)
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось обновить характеристики артикула",
                )

    @classmethod
    async def delete_article(cls, request: Request, article_id: int):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут удалять артикулы"
            )

        async with new_session() as db:
            article = await db.get(Article, article_id)
            if not article:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Артикул не найден"
                )

            await db.delete(article)
            try:
                await db.commit()
                return {"message": "Артикул успешно удалён"}
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось удалить артикул",
                )
