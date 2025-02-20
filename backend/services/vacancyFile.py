from fastapi import HTTPException, status, Request, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import Vacancy as VacancyModel, Resume as ResumeModel
from schemas import *
from database import new_session
from typing import Dict, Any
from Function import Functions
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication





class VacancyService:
    @classmethod
    async def create_vacancy(cls, request: Request, vacancy: VacancyCreate) -> Vacancy:
        user_data = await Functions.get_user_data(request)  # Используем функцию из модуля Functions
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Только администраторы могут добавлять вакансии"
            )

        async with new_session() as db:
            db_vacancy = VacancyModel(**vacancy.dict())
            db.add(db_vacancy)
            try:
                await db.commit()
                await db.refresh(db_vacancy)
                return Vacancy(**db_vacancy.__dict__)
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось добавить вакансию",
                )

    @classmethod
    async def get_vacancies(cls) -> list[Vacancy]:
        async with new_session() as db:
            vacancies = await db.execute(select(VacancyModel))
            return [Vacancy(**vacancy.__dict__) for vacancy in vacancies.scalars().all()]

    @classmethod
    async def get_vacancy(cls, vacancy_id: int) -> Vacancy:
        async with new_session() as db:
            result = await db.execute(select(VacancyModel).where(VacancyModel.id == vacancy_id))
            db_vacancy = result.scalars().first()
            if not db_vacancy:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Вакансия не найдена"
                )
            return Vacancy.from_orm(db_vacancy)

    @classmethod
    async def update_vacancy(cls, request: Request, vacancy_id: int, vacancy_update: VacancyUpdate) -> Vacancy:
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Только администраторы могут изменять вакансии"
            )

        async with new_session() as db:
            db_vacancy = await db.execute(select(VacancyModel).where(VacancyModel.id == vacancy_id))
            db_vacancy = db_vacancy.scalars().first()
            if not db_vacancy:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Вакансия не найдена"
                )

            update_data = vacancy_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_vacancy, key, value)

            try:
                await db.commit()
                await db.refresh(db_vacancy)
                return Vacancy.from_orm(db_vacancy)
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось обновить вакансию",
                )

    @classmethod
    async def delete_vacancy(cls, request: Request, vacancy_id: int):
        user_data = await Functions.get_user_data(request)
        if user_data["user_role"] != "Админ":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Только администраторы могут удалять вакансии"
            )

        async with new_session() as db:
            db_vacancy = await db.execute(select(VacancyModel).where(VacancyModel.id == vacancy_id))
            db_vacancy = db_vacancy.scalars().first()
            if not db_vacancy:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Вакансия не найдена"
                )

            await db.delete(db_vacancy)
            try:
                await db.commit()
                return {"message": "Вакансия успешно удалена"}
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось удалить вакансию",
                )

    async def send_resume_email(resume: ResumeCreate, file_path: str):
        """Отправляет резюме по электронной почте."""
        sender_email = "dart_side34@mail.ru"  # Замените на вашу почту
        sender_password = "N5FinwTdTQpdnVqb0WHS"  # Замените на ваш пароль
        receiver_emails = ["dart_side34@mail.ru"]  # Список адресов

        message = MIMEMultipart()
        message["Subject"] = "Новое резюме от пользователя"
        message["From"] = sender_email
        message["To"] = ", ".join(receiver_emails)

        text = f"""
            Новое резюме:
            Имя: {resume.name}
            Город: {resume.city}
            Вакансия: {resume.vacancy}
            Телефон: {resume.phone}
            Комментарий: {resume.comment}
            """

        message.attach(MIMEText(text, "plain"))

        # Добавляем файл резюме
        try:
            with open(file_path, "rb") as f:
                resume_attachment = MIMEApplication(f.read(), _subtype="pdf")
                resume_attachment.add_header('Content-Disposition', 'attachment', filename=resume.file_name)
                message.attach(resume_attachment)
        except FileNotFoundError:
            print(f"Ошибка: Файл не найден по пути {file_path}")
            return  # Прерываем отправку, если файл не найден

        try:
            with smtplib.SMTP_SSL("smtp.mail.ru", 465) as server:
                server.login(sender_email, sender_password)
                for receiver_email in receiver_emails:
                    server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email уведомление с резюме отправлено!")
        except Exception as e:
            print(f"Ошибка отправки email: {e}")

    async def create_resume(resume: ResumeCreate, resume_file: UploadFile) -> Resume:


        upload_dir = "C:\\Users\\user\\Documents\\GitHub\\uni-practice\\backend\\resumes"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        file_path = os.path.join(upload_dir, resume_file.filename)
        try:
            with open(file_path, "wb") as buffer:
                content = await resume_file.read()
                buffer.write(content)
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Не удалось сохранить файл резюме",
            )

        resume.file_name = resume_file.filename

        async with new_session() as db:
            db_resume = ResumeModel(
                city=resume.city,
                name=resume.name,
                vacancy=resume.vacancy,
                phone=resume.phone,
                comment=resume.comment,
                file_name=resume.file_name
            )

            db.add(db_resume)
            try:
                await db.commit()
                await db.refresh(db_resume)
                await VacancyService.send_resume_email(resume, file_path)
                os.remove(file_path)
                return Resume.from_orm(db_resume)
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось добавить резюме",
                )