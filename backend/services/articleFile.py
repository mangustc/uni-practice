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
            subcategory = await db.execute(
                select(Subcategory).where(Subcategory.name == data.subcategory_name)
            )
            subcategory = subcategory.scalars().first()
            if subcategory is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Подкатегории с таким именем не существует",
                )

            new_article = Article(subcategory_id=subcategory.id, description=data.description,
                                  characteristics=data.characteristics, price=data.price)
            db.add(new_article)
            try:
                await db.commit()
                await db.refresh(new_article)
                return ArticleResponse(article_id=new_article.id)  # Return правильный формат
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
            "subcategory_id": article.subcategory_id,
            "article_description": article.description,
            "article_characteristics": article.characteristics,
            "article_price": article.price
        }  # Correct format

    @classmethod
    async def get_all_articles(cls):
        query = select(Article)
        async with new_session() as db:
            result = await db.execute(query)
        articles = result.scalars().all()
        return [
            {"subcategory_id": a.subcategory_id,
             "article_description": a.description,
             "article_characteristics": a.characteristics,
             "article_price": a.price} for a in articles
        ]  # Correct format

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

            subcategory = await db.execute(
                select(Subcategory).where(Subcategory.name == data.subcategory_name)
            )
            subcategory = subcategory.scalars().first()
            if subcategory is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Подкатегории с таким именем не существует",
                )

            old_article.subcategory_id = subcategory.id
            old_article.description = data.description
            old_article.characteristics = data.characteristics
            old_article.price = data.price
            try:
                await db.commit()
                await db.refresh(old_article)
                return ArticleResponse(article_id=old_article.id)  # Return правильный формат
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось обновить информацию об артикуле",
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

            await db.delete(article)  # Correct delete
            try:
                await db.commit()
                return {"message": "Артикул успешно удалён"}  # Правильный формат
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось удалить артикул",
                )