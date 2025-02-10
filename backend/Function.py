from fastapi import HTTPException, Request
import jwt

SECRET_KEY = "manilovefishing"
ALGORITHM = "HS256"

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