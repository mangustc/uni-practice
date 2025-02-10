from fastapi import HTTPException, status, Request
from database import new_session, Subcategory, Category
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, and_
from schemas import AddSubcategory, SubcategoryResponse
from Function import Functions



class SubcategoryService:
    @classmethod
    async def add_subcategory(cls, subcategory: AddSubcategory, request: Request):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403,
                detail="Только администраторы могут добавлять подкатегории",
            )

        async with new_session() as db:
            # Check if category exists
            category = await db.get(Category, subcategory.category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Категория не найдена"
                )

            # Check if subcategory name already exists in the same category
            existing_subcategory = await db.execute(
                select(Subcategory).where(
                    and_(
                        Subcategory.name == subcategory.name,
                        Subcategory.category_id == subcategory.category_id,
                    )
                )
            )
            if existing_subcategory.scalars().first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Подкатегория с таким именем уже существует в этой категории",
                )

            new_subcategory = Subcategory(
                name=subcategory.name, category_id=subcategory.category_id
            )
            db.add(new_subcategory)
            try:
                await db.commit()
                await db.refresh(new_subcategory)
                return SubcategoryResponse(
                    subcategory_id=new_subcategory.id,
                    subcategory_name=new_subcategory.name,
                    category_id=new_subcategory.category_id,
                )
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось добавить подкатегорию",
                )

    @classmethod
    async def get_subcategory(cls, subcategory_id: int):
        async with new_session() as db:
            result = await db.execute(
                select(Subcategory).where(Subcategory.id == subcategory_id)
            )
            subcategory = result.scalars().first()
            if not subcategory:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Подкатегория не найдена"
                )
            return {
                "subcategory_id": subcategory.id,
                "subcategory_name": subcategory.name,
                "category_id": subcategory.category_id,
            }

    @classmethod
    async def get_all_subcategories(cls):
        async with new_session() as db:
            result = await db.execute(select(Subcategory))
            subcategories = result.scalars().all()
            return [
                {
                    "subcategory_id": s.id,
                    "subcategory_name": s.name,
                    "category_id": s.category_id,
                }
                for s in subcategories
            ]

    @classmethod
    async def update_subcategory(
        cls, subcategory_id: int, new_name: str, request: Request, category_id: int
    ):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403,
                detail="Только администраторы могут изменять подкатегории",
            )

        async with new_session() as db:
            subcategory = await db.get(Subcategory, subcategory_id)
            if not subcategory:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Подкатегория не найдена"
                )

            category = await db.get(Category, category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Категория не найдена"
                )

            # Check if the new name already exists for another subcategory in the same category
            existing_subcategory = await db.execute(
                select(Subcategory).where(
                    and_(
                        Subcategory.name == new_name,
                        Subcategory.category_id == category_id,
                        Subcategory.id != subcategory_id,
                    )
                )
            )
            if existing_subcategory.scalars().first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Подкатегория с таким именем уже существует в этой категории",
                )

            subcategory.name = new_name
            subcategory.category_id = category_id
            try:
                await db.commit()
                await db.refresh(subcategory)
                return SubcategoryResponse(
                    subcategory_id=subcategory.id,
                    subcategory_name=subcategory.name,
                    category_id=subcategory.category_id,
                )
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось обновить подкатегорию",
                )

    @classmethod
    async def delete_subcategory(cls, subcategory_id: int, request: Request):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=403,
                detail="Только администраторы могут удалять подкатегории",
            )

        async with new_session() as db:
            subcategory = await db.get(Subcategory, subcategory_id)
            if not subcategory:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Подкатегория не найдена"
                )

            await db.delete(subcategory)
            try:
                await db.commit()
                return {"message": "Подкатегория успешно удалена"}
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось удалить подкатегорию",
                )