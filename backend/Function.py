from fastapi import HTTPException, Request
from sqlalchemy import update, select
from database import Product, new_session
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import jwt

SECRET_KEY = "manilovefishing"
ALGORITHM = "HS256"


async def deactivate_expired_new_products():
    async with new_session() as db:
        print("Checking for expired 'new' products...")  # Added logging

        expired_products = await db.execute(
            select(Product).where(Product.new == True, Product.new_until <= datetime.now()) #compare datetime
        )
        expired_products = expired_products.scalars().all()
        print(f"Found {len(expired_products)} expired products.")

        for product in expired_products:
            product.new = False
            product.new_until = None
            print(f"Deactivating product {product.id}")

        try:
            await db.commit()
            print("Deactivated expired 'new' products.")
        except SQLAlchemyError as e:
            await db.rollback()
            print(f"Error deactivating expired 'new' products: {e}")


class Functions:
    @staticmethod
    async def get_user_data(request: Request):
        token = request.cookies.get("token")
        if token is None:
            raise HTTPException(status_code=401, detail="Необходима авторизация")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("id")
            user_role = payload.get("role")  # Получаем роль из токена

            if user_id is None or user_role is None:
                raise HTTPException(status_code=401, detail="Не удалось извлечь user_id или role из токена")

            return {"user_id": user_id, "user_role": user_role}  # Возвращаем и user_id, и role

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Срок действия токена истек")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Неверный токен")


