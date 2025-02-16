import os
from datetime import date
from typing import Sequence
from fastapi import UploadFile, HTTPException, status, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import joinedload, contains_eager
from database import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete, Select, and_
from schemas import *
from Function import Functions
from uuid import uuid4
import shutil


class ArticleService:
    @classmethod
    async def create_article(cls, request: Request):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут добавлять категории"
            )

        async with new_session() as db:
            new_article = Article()
            db.add(new_article)
            try:
                await db.commit()
                await db.refresh(new_article)
                return GetArticleResponse(article_id=new_article.id)
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось добавить артикул",
                )

    @classmethod
    async def get_all_articles(cls):
        query = select(Article)
        async with new_session() as db:
            result = await db.execute(query)
        articles = result.scalars().all()
        return [GetArticleResponse(article_id=a.id).__dict__ for a in articles]

    @classmethod
    async def delete_article(cls, request: Request, article_id: int):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут удалять артикулы"
            )
        query = delete(Article).where(Article.id == article_id).returning(Article.id)
        async with new_session() as db:
            result = await db.execute(query)
            if result.scalars().first() is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Артикул не найден"
                )
            try:
                await db.commit()
                return {"message": "Артикул успешно удалён"}
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось удалить артикул",
                )
