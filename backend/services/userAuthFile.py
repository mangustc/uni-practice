from datetime import timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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
                "user_id": new_user.id,
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
                "user_id": new_user.id,
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
                "role": user.role.value  # Добавляем роль в токен
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
                "user_id": user.id,
                "email": user.email,
                "name": user.name,
                "surname": user.surname,
                "number": user.number,
                "role": user.role.value
            }

    @classmethod
    async def update_user_info(cls, request: Request, user_update: UpdateUserInfoRequest):
        user_data = await Functions.get_user_data(request)
        user_id = user_data["user_id"]

        async with new_session() as db:
            old_user = await db.get(User, user_id)
            if old_user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Пользователь не найден",
                )

            update_data = user_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                if key == "password":
                    if value == "" or user_update.confirm_password == "":
                        # Не обновляем пароль, если переданы пустые строки
                        continue
                    elif value != user_update.confirm_password:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Пароли не совпадают",
                        )
                    # Хеширование пароля с помощью bcrypt
                    salt = bcrypt.gensalt()
                    hashed_password = bcrypt.hashpw(value.encode('utf-8'), salt)
                    setattr(old_user, key,
                            hashed_password.decode('utf-8'))  # Сохранение хешированного пароля в виде строки
                elif key == "email":
                    # Не обновляем email
                    continue
                else:
                    setattr(old_user, key, value)

            try:
                await db.commit()
                await db.refresh(old_user)
                return {"message": "Данные пользователя обновлены успешно"}
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось обновить данные пользователя",
                )

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
    async def change_role(cls, new_role: str, request: Request, response: Response):
        user_data = await Functions.get_user_data(request)
        user_id = user_data["user_id"]
        # user_role = user_data["user_role"]  # Не нужно использовать старую роль из кук

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

            user.role = new_role
            try:
                await db.commit()
                await db.refresh(user)  # Обновляем объект user после коммита
            except IntegrityError as e:
                await db.rollback()
                raise HTTPException(
                    status_code=500, detail=f"Ошибка при изменении роли пользователя: {e}"
                )

            # Обновляем куки с новой ролью
            token_data = {
                "id": user.id,
                "email": user.email,
                "role": user.role.value
            }
            token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
            response.set_cookie(key="token", value=token, httponly=True, secure=False)

            return {"message": f"Роль пользователя с ID {user_id} успешно изменена на {new_role}."}

    @classmethod
    async def request_password_reset(cls, email: str):
        async with new_session() as db:
            result = await db.execute(select(User).where(User.email == email))
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=400, detail="Пользователь не найден")

            # Генерируем токен сброса пароля
            token_data = {
                "email": email,
                "exp": datetime.utcnow() + timedelta(minutes=30)  # Время жизни токена 30 минут
            }
            token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

            # Сохраняем токен в базе данных
            password_reset = PasswordReset(
                user_id=user.id,
                token=token
            )
            db.add(password_reset)
            try:
                await db.commit()
            except IntegrityError:
                await db.rollback()
                raise HTTPException(status_code=500, detail="Ошибка при сохранении токена сброса пароля")

            # Отправляем письмо с токеном
            await cls.send_reset_password_email(email, token)

            return {"message": "Ссылка для сброса пароля отправлена на ваш email."}

    @classmethod
    async def reset_password(cls, token: str, new_password: str):
        try:
            token_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=400, detail="Срок действия токена истек")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=400, detail="Некорректный токен")

        async with new_session() as db:
            result = await db.execute(select(PasswordReset).where(PasswordReset.token == token))
            password_reset = result.scalars().first()
            if not password_reset:
                raise HTTPException(status_code=400, detail="Токен не найден")

            user_id = password_reset.user_id
            user = await db.get(User, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="Пользователь не найден")

            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user.password = hashed_password

            try:
                await db.delete(password_reset)  # Удаляем токен сброса пароля
                await db.commit()
            except IntegrityError:
                await db.rollback()
                raise HTTPException(status_code=500, detail="Ошибка при сбросе пароля")

            return {"message": "Новый пароль успешно установлен"}

    @classmethod
    async def send_reset_password_email(cls, email: str, token: str):
        msg = MIMEMultipart()
        msg['From'] = 'dart_side34@mail.ru'
        msg['To'] = email
        msg['Subject'] = 'Сброс пароля'

        # reset_link = f"http://localhost:8000/api/user/reset_password/{token}"
        reset_link = f"http://localhost:5173/reset-password/{token}"
        body = f"Ссылка для сброса пароля: {reset_link}"
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP_SSL("smtp.mail.ru", 465)
        server.login(msg['From'], 'N5FinwTdTQpdnVqb0WHS')
        text = msg.as_string()
        server.sendmail(msg['From'], msg['To'], text)
        server.quit()