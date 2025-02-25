import os
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status, UploadFile, Request
from fastapi.responses import FileResponse
from schemas import ShopCreate, ShopUpdate, ShopResponse
from database import new_session, Shop
from Function import Functions

class ShopService:
    @classmethod
    async def create_shop(cls, request: Request, shop: ShopCreate) -> ShopResponse:
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Только администраторы могут добавлять магазины"
            )
        async with new_session() as db:
            db_shop = Shop(**shop.dict(exclude={"photo_path"}))  # исключаем photo_path
            db.add(db_shop)
            try:
                await db.commit()
                await db.refresh(db_shop)
                return ShopResponse.from_orm(db_shop)
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось добавить магазин",
                )

    @classmethod
    async def get_shops(cls) -> list[ShopResponse]:
        async with new_session() as db:
            shops = await db.execute(select(Shop))
            return [ShopResponse.from_orm(shop) for shop in shops.scalars().all()]

    @classmethod
    async def get_shop(cls, shop_id: int) -> ShopResponse:
        async with new_session() as db:
            result = await db.execute(select(Shop).where(Shop.id == shop_id))
            db_shop = result.scalars().first()
            if not db_shop:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Магазин не найден"
                )
            return ShopResponse.from_orm(db_shop)

    @classmethod
    async def update_shop(cls, request: Request, shop_id: int, shop_update: ShopUpdate) -> ShopResponse:
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Только администраторы могут обновлять информацию о магазине"
            )
        async with new_session() as db:
            result = await db.execute(select(Shop).where(Shop.id == shop_id))
            db_shop = result.scalars().first()

            if not db_shop:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Магазин не найден"
                )

            update_data = shop_update.dict(exclude_unset=True, exclude={"photo_path"})  # исключаем photo_path
            for key, value in update_data.items():
                setattr(db_shop, key, value)

            try:
                await db.commit()
                await db.refresh(db_shop)
                return ShopResponse.from_orm(db_shop)
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось обновить магазин",
                )

    @classmethod
    async def delete_shop(cls, request: Request, shop_id: int) -> dict:
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Только администраторы могут обновлять фото магазина"
            )
        async with new_session() as db:
            result = await db.execute(select(Shop).where(Shop.id == shop_id))
            db_shop = result.scalars().first()

            if not db_shop:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Магазин не найден"
                )

            await db.delete(db_shop)
            try:
                await db.commit()
                return {"message": "Магазин успешно удален"}
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось удалить магазин",
                )

    @classmethod
    async def get_shop_photo(cls, shop_id: int):
        query = select(Shop).where(Shop.id == shop_id)
        async with new_session() as db:
            result = await db.execute(query)
        shop = result.scalars().first()
        if not shop:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Магазин не найден"
            )
        if shop.photo_path is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Изображение магазина не было найдено"
            )
        return FileResponse(shop.photo_path)

    import os

    @classmethod
    async def update_shop_photo(cls, request: Request, shop_id: int, file: UploadFile):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Только администраторы могут обновлять фото магазина"
            )
        if "image" not in file.content_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Файл не является изображением"
            )
        if file.size > 3145728:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Файл превышает размер в 3МБ"
            )

        # Определите абсолютный путь к папке images
        project_root = "C:\\Users\\user\\Documents\\GitHub\\uni-practice\\backend"
        upload_dir = os.path.join(project_root, "images", "shops")

        # Создайте папку, если она не существует
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        file_extension = file.filename.split('.')[-1]
        file_path = os.path.join(upload_dir, f"{shop_id}.{file_extension}")

        async with new_session() as db:
            shop = await db.execute(
                select(Shop).where(Shop.id == shop_id)
            )
            shop = shop.scalars().first()
            if shop is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Такого магазина не существует",
                )
            if shop.photo_path is not None:
                if os.path.exists(shop.photo_path):
                    os.remove(shop.photo_path)

            try:
                contents = await file.read()
                with open(file_path, "wb") as f:
                    f.write(contents)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f'Что-то пошло не так: {e}')
            finally:
                await file.close()

            shop.photo_path = file_path
            await db.commit()

        return {"message": f"Файл загружен {file_path}"}


    @classmethod
    async def delete_shop_photo(cls, request: Request, shop_id: int) -> dict:
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Только администраторы могут удалять фото магазина"
            )
        async with new_session() as db:
            shop = await db.execute(
                select(Shop).where(Shop.id == shop_id)
            )
            shop = shop.scalars().first()
            if shop is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Такого магазина не существует",
                )
            if shop.photo_path is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="У магазина нет фотографии",
                )
            if os.path.exists(shop.photo_path):
                os.remove(shop.photo_path)
            shop.photo_path = None
            await db.commit()
        return {"message": "Фотография магазина успешно удалена"}
