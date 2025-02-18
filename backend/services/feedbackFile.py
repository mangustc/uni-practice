from typing import List

from fastapi import HTTPException, Request
from sqlalchemy import select
from starlette import status

from Function import Functions
from database import Feedback, new_session
from schemas import FeedbackCreate, FeedbackResponse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class FeedbackService:
    @classmethod
    async def create_feedback(cls, feedback: FeedbackCreate):
        async with new_session() as db:
            db_feedback = Feedback(**feedback.dict())
            db.add(db_feedback)
            await db.commit()
            await db.refresh(db_feedback)

            await cls.send_email_notification(db_feedback)

            return db_feedback

    @classmethod
    async def send_email_notification(cls, feedback: FeedbackResponse):
        sender_email = "dart_side34@mail.ru"  # Замените на вашу почту
        sender_password = "N5FinwTdTQpdnVqb0WHS"  # Замените на ваш пароль
        receiver_emails = ["dart_side34@mail.ru"]  # Список адресов

        message = MIMEMultipart("alternative")
        message["Subject"] = "Новая обратная связь от пользователя"
        message["From"] = sender_email
        message["To"] = ", ".join(receiver_emails)  # Перечисляем адресатов через запятую для заголовка

        text = f"""
            Новая обратная связь:
            Имя: {feedback.name}
            Email: {feedback.email}
            Телефон: {feedback.phone}
            Комментарий: {feedback.comment}
            """

        part1 = MIMEText(text, "plain")
        message.attach(part1)

        try:
            with smtplib.SMTP_SSL("smtp.mail.ru", 465) as server:
                server.login(sender_email, sender_password)
                for receiver_email in receiver_emails:
                    server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email уведомление отправлено!")
        except Exception as e:
            print(f"Ошибка отправки email: {e}")

    @classmethod
    async def get_all_feedback(cls, request: Request) -> List[FeedbackResponse]:
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Только администраторы могут просматривать обратную связь"
            )

        async with new_session() as db:
            result = await db.execute(select(Feedback))
            feedbacks = result.scalars().all()
            # Преобразуем объекты Feedback в FeedbackResponse
            return [FeedbackResponse.from_orm(feedback) for feedback in feedbacks]

    @classmethod
    async def get_feedback_by_id(cls, feedback_id: int, request: Request) -> FeedbackResponse:
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Только администраторы могут просматривать обратную связь"
            )

        async with new_session() as db:
            feedback = await db.get(Feedback, feedback_id)
            if not feedback:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Обратная связь не найдена"
                )
            return FeedbackResponse.from_orm(feedback)

    @classmethod
    async def process_feedback(cls, feedback_id: int, request: Request) -> FeedbackResponse:
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Только администраторы могут изменять статус обратной связи"
            )

        async with new_session() as db:
            feedback = await db.get(Feedback, feedback_id)
            if not feedback:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Обратная связь не найдена"
                )
            feedback.is_processed = True
            await db.commit()
            await db.refresh(feedback)
            return FeedbackResponse.from_orm(feedback)