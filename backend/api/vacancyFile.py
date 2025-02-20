from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File
from schemas import *
from services import VacancyService
from services import VacancyService

router = APIRouter(tags=["Vacancy-Resume"])

@router.post("/vacancies/", response_model=Vacancy)
async def create_vacancy_endpoint(request: Request, vacancy: VacancyCreate):
    return await VacancyService.create_vacancy(request=request, vacancy=vacancy)

@router.get("/vacancies/", response_model=list[Vacancy])
async def read_vacancies():
    return await VacancyService.get_vacancies()

@router.get("/vacancies/{vacancy_id}", response_model=Vacancy)
async def read_vacancy(vacancy_id: int):
    return await VacancyService.get_vacancy(vacancy_id=vacancy_id)


@router.put("/vacancies/{vacancy_id}", response_model=Vacancy)
async def update_vacancy_endpoint(request: Request, vacancy_id: int, vacancy_update: VacancyUpdate):
    return await VacancyService.update_vacancy(request=request, vacancy_id=vacancy_id, vacancy_update=vacancy_update)

@router.delete("/vacancies/{vacancy_id}")
async def delete_vacancy_endpoint(request: Request, vacancy_id: int):
    return await VacancyService.delete_vacancy(request=request, vacancy_id=vacancy_id)



@router.post("/resumes/", response_model=Resume)
async def create_resume_endpoint(
    city: str,
    name: str,
    vacancy: str,
    phone: str,
    comment: str | None = None,
    resume_file: UploadFile = File(...)
):
    resume_data = ResumeCreate(
        city=city,
        name=name,
        vacancy=vacancy,
        phone=phone,
        comment=comment
    )
    return await VacancyService.create_resume(resume=resume_data, resume_file=resume_file)