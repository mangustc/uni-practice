from database import WholesaleBuyer, new_session
from schemas import WholesaleBuyerCreate, WholesaleBuyerResponse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class WholesaleBuyerService:
    @classmethod
    async def create_wholesale_buyer(cls, wholesale_buyer: WholesaleBuyerCreate):
        async with new_session() as db:
            db_wholesale_buyer = WholesaleBuyer(**wholesale_buyer.dict())
            db.add(db_wholesale_buyer)
            await db.commit()
            await db.refresh(db_wholesale_buyer)

            await cls.send_email_notification(db_wholesale_buyer)

            return db_wholesale_buyer

    @classmethod
    async def send_email_notification(cls, wholesale_buyer: WholesaleBuyerResponse):
        sender_email = "dart_side34@mail.ru"
        sender_password = "N5FinwTdTQpdnVqb0WHS"
        receiver_emails = ["dart_side34@mail.ru"]

        message = MIMEMultipart("alternative")
        message["Subject"] = "Новая заявка от оптового покупателя"
        message["From"] = sender_email
        message["To"] = ", ".join(receiver_emails)

        text = f"""
            Новая заявка от оптового покупателя:
            Имя: {wholesale_buyer.name}
            Email: {wholesale_buyer.email}
            Телефон: {wholesale_buyer.phone}
            Комментарий: {wholesale_buyer.comment}
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

