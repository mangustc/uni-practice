from fastapi import HTTPException, status, Response, Request
from database import *
from schemas import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import select, delete
import bcrypt
import jwt
from Function import Functions

SECRET_KEY = "manilovefishing"
ALGORITHM = "HS256"


class UserService:
    @classmethod
    async def registration(cls, user: Registr):
        async with new_session() as db:
            result = await db.execute(select(User).where(User.email == user.email))
            existing_user = result.scalars().first()
            if existing_user:
                raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
            if user.password != user.re_password:
                raise HTTPException(status_code=400, detail="Пароли не совпадают")

            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            new_user = User(
                email=user.email,
                password=hashed_password,
                number=user.number,
                role="Пользователь",
            )
            db.add(new_user)

            try:
                await db.commit()
                await db.refresh(new_user)  # Обновляем объект, чтобы получить ID
            except IntegrityError:
                await db.rollback()
                raise HTTPException(status_code=500, detail="Ошибка при сохранении пользователя")

            return {
                "id": new_user.id,
                "email": new_user.email,
                "message": "Пользователь успешно зарегистрирован."
            }

    @classmethod
    async def registration_legal_entity(cls, user: RegistrLegalEntity):
        return await UserService.registration_legal_entity_or_ip(user, "Юр.лицо")

    @classmethod
    async def registration_ip(cls, user: RegistrLegalEntity):
        return await UserService.registration_legal_entity_or_ip(user, "ИП")

    @classmethod
    async def registration_legal_entity_or_ip(cls, user: RegistrLegalEntity, role: str):
        async with new_session() as db:
            result = await db.execute(select(User).where(User.email == user.email))
            existing_user = result.scalars().first()
            if existing_user:
                raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
            if user.password != user.re_password:
                raise HTTPException(status_code=400, detail="Пароли не совпадают")
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            new_user = User(
                email=user.email,
                password=hashed_password,
                number=user.number,
                role=role,
                organization_name=user.organization_name,
                INN=user.INN
            )
            db.add(new_user)
            try:
                await db.commit()
                await db.refresh(new_user)  # Обновляем объект, чтобы получить ID
            except IntegrityError:
                await db.rollback()
                raise HTTPException(status_code=500, detail="Ошибка при сохранении пользователя")
            return {
                "id": new_user.id,
                "email": new_user.email,
                "message": "Пользователь успешно зарегистрирован."
            }

    @classmethod
    async def login(cls, login_data: Login, response: Response):
        async with new_session() as db:
            result = await db.execute(select(User).where(User.email == login_data.email))
            try:
                user = result.scalars().one()
            except NoResultFound:
                raise HTTPException(status_code=400, detail="Неверный email или пароль")

            if not bcrypt.checkpw(login_data.password.encode('utf-8'), user.password.encode('utf-8')):
                raise HTTPException(status_code=400, detail="Неверный email или пароль")

            token_data = {
                "id": user.id,
                "email": user.email,
                "role": user.role  # Добавляем роль в токен
            }
            token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
            response.set_cookie(key="token", value=token, httponly=True, secure=False)
            return {
                "email": user.email,
                "token": token,
                "message": "Пользователь успешно авторизован."
            }

    @classmethod
    async def logout(cls, response: Response):
        response.delete_cookie(key="token")
        return {"message": "Пользователь успешно вышел из системы."}

    @classmethod
    async def update_number(cls, new_number: str, request: Request):
        user_data = await Functions.get_user_data(request)
        user_id = user_data["user_id"]
        async with new_session() as db:
            user = await db.get(User, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="Пользователь не найден")

            # Валидация номера телефона
            pattern = r"^\+7\(\d{3}\)\-\d{3}\-\d{2}\-\d{2}$"
            if not re.match(pattern, new_number):
                raise HTTPException(status_code=400, detail="Некорректный формат номера телефона")

            user.number = new_number
            try:
                await db.commit()
            except IntegrityError:
                await db.rollback()
                raise HTTPException(status_code=500, detail="Ошибка при обновлении номера телефона")

            return {"message": "Номер телефона успешно обновлен"}

    @classmethod
    async def update_name(cls, new_name: str, request: Request):
        user_data = await Functions.get_user_data(request)
        user_id = user_data["user_id"]
        async with new_session() as db:
            user = await db.get(User, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="Пользователь не найден")

            user.name = new_name
            try:
                await db.commit()
            except IntegrityError:
                await db.rollback()
                raise HTTPException(status_code=500, detail="Ошибка при обновлении имени")

            return {"message": "Имя успешно обновлено"}

    @classmethod
    async def update_surname(cls, new_surname: str, request: Request):
        user_data = await Functions.get_user_data(request)
        user_id = user_data["user_id"]
        async with new_session() as db:
            user = await db.get(User, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="Пользователь не найден")

            user.surname = new_surname
            try:
                await db.commit()
            except IntegrityError:
                await db.rollback()
                raise HTTPException(status_code=500, detail="Ошибка при обновлении фамилии")

            return {"message": "Фамилия успешно обновлена"}

    @classmethod
    async def get_user_info(cls, request: Request):
        user_data = await Functions.get_user_data(request)
        user_id = user_data["user_id"]
        async with new_session() as db:
            result = await db.execute(select(User).where(User.id == user_id))
            user = result.scalars().first()

            if not user:
                raise HTTPException(status_code=404, detail="Пользователь не найден")

            return {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "surname": user.surname,
                "number": user.number,
                "role": user.role
            }

    @classmethod
    async def delete_account(cls, request: Request, response: Response):
        user_data = await Functions.get_user_data(request)
        user_id = user_data["user_id"]

        async with new_session() as db:
            user = await db.get(User, user_id)

            if not user:
                raise HTTPException(status_code=404, detail="Пользователь не найден")

            try:
                await db.delete(user)
                await db.commit()
                await cls.logout(response)

                return {"message": f"Аккаунт пользователя с ID {user_id} успешно удален."}
            except IntegrityError as e:
                await db.rollback()
                raise HTTPException(status_code=500, detail=f"Ошибка при удалении пользователя: {e}")

    @classmethod
    async def change_role(cls, new_role: str, request: Request):
        user_data = await Functions.get_user_data(request)
        user_id = user_data["user_id"]
        user_role = user_data["user_role"]

        valid_roles = ["Пользователь", "Юр.лицо", "Админ", "ИП"]
        if new_role not in valid_roles:
            raise HTTPException(
                status_code=400,
                detail=f"Некорректная роль: {new_role}. Допустимые роли: {valid_roles}",
            )

        async with new_session() as db:
            user = await db.get(User, user_id)

            if not user:
                raise HTTPException(status_code=404, detail="Пользователь не найден")

            # if user_role != "Админ":
            #     raise HTTPException(
            #         status_code=403,
            #         detail="Недостаточно прав для изменения роли пользователя.",
            #     )

            user.role = new_role
            try:
                await db.commit()
            except IntegrityError as e:
                await db.rollback()
                raise HTTPException(
                    status_code=500, detail=f"Ошибка при изменении роли пользователя: {e}"
                )

            return {"message": f"Роль пользователя с ID {user_id} успешно изменена на {new_role}."}
