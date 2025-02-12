from fastapi import HTTPException, status, Request
from database import new_session, Category
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, and_
from schemas import *
from Function import Functions


class CategoryService:
    @classmethod
    async def add_category_root(cls, category: AddCategoryRoot, request: Request):
        data = AddCategory(name=category.name, category_name_parent=None)
        return await CategoryService.add_category(data, request)

    @classmethod
    async def add_category(cls, category: AddCategory, request: Request):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут добавлять категории"
            )

        async with new_session() as db:
            # Check if category name already exists
            existing_category = await db.execute(
                select(Category).where(Category.name == category.name)
            )
            if existing_category.scalars().first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Категория с таким именем уже существует",
                )
            if category.category_name_parent is not None:
                query = select(Category).where(Category.name == category.category_name_parent)
                result = await db.execute(query)
                result = result.scalars().first()
                if result is None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Категории, на которую вы ссылаетесь, не существует",
                    )
                parent_id = result.id
            else:
                parent_id = None
            new_category = Category(name=category.name, parent_id=parent_id)
            db.add(new_category)
            try:
                await db.commit()
                await db.refresh(new_category)
                return CategoryResponse(
                    category_id=new_category.id, category_name=new_category.name, category_parent_id=parent_id
                )  # Return правильный формат
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось добавить категорию",
                )

    @classmethod
    async def get_category(cls, category_id: int):
        async with new_session() as db:
            result = await db.execute(select(Category).where(Category.id == category_id))
            category = result.scalars().first()
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена"
                )
            return {
                "category_id": category.id,
                "category_name": category.name,
                "category_parent_id": category.parent_id
            }  # Correct format

    @classmethod
    async def get_all_categories(cls):
        async with new_session() as db:
            result = await db.execute(select(Category))
            categories = result.scalars().all()
            return [
                {"category_id": c.id,
                 "category_name": c.name,
                 "category_parent_id": c.parent_id} for c in categories
            ]  # Correct format

    @classmethod
    async def get_category_roots(cls):
        async with new_session() as db:
            query = select(Category).where(Category.parent_id == None)
            result = await db.execute(query)
            result = result.scalars().all()
            return [
                {"category_id": c.id,
                 "category_name": c.name,
                 "category_parent_id": c.parent_id} for c in result
            ]  # Correct format

    @classmethod
    async def get_categories_by_category_name_parent(cls, category_name_parent: str):
        query = select(Category).where(Category.name == category_name_parent)
        async with new_session() as db:
            result = await db.execute(query)
            result = result.scalars().first()
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена"
                )
            query = select(Category).where(Category.parent_id == result.id)
            result = await db.execute(query)
            result = result.scalars().all()
            return [
                {"category_id": c.id,
                 "category_name": c.name,
                 "category_parent_id": c.parent_id} for c in result
            ]  # Correct format

    @classmethod
    async def update_category(
            cls, category_id: int, new_name: str, request: Request
    ):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут изменять категории"
            )

        async with new_session() as db:
            category = await db.get(Category, category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена"
                )

            # Check if the new name already exists for another category
            existing_category = await db.execute(
                select(Category).where(
                    and_(Category.name == new_name, Category.id != category_id)
                )
            )
            if existing_category.scalars().first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Категория с таким именем уже существует",
                )

            category.name = new_name  # Correct update
            try:
                await db.commit()
                await db.refresh(category)
                return CategoryResponse(
                    category_id=category.id, category_name=category.name, category_parent_id=category.parent_id
                )  # Правильный формат
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось обновить категорию",
                )

    @classmethod
    async def delete_category(cls, category_id: int, request: Request):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403, detail="Только администраторы могут удалять категории"
            )

        async with new_session() as db:
            category = await db.get(Category, category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена"
                )

            await db.delete(category)  # Correct delete
            try:
                await db.commit()
                return {"message": "Категория успешно удалена"}  # Правильный формат
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось удалить категорию",
                )

