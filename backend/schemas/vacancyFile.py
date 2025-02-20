from pydantic import BaseModel
from typing import Optional

class VacancyBase(BaseModel):
    title: str
    description: str
    requirements: str
    responsibilities: str
    salary: Optional[str] = None

class VacancyCreate(VacancyBase):
    pass

class Vacancy(VacancyBase):
    id: int

    class Config:
        from_attributes = True

class VacancyUpdate(VacancyBase):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    salary: Optional[str] = None


# --- Схемы для резюме ---
class ResumeBase(BaseModel):
    city: str
    name: str
    vacancy: str  # Либо ID вакансии, либо название
    phone: str
    comment: Optional[str] = None
    file_name: str = "default_resume.pdf"

class ResumeCreate(ResumeBase):
    pass

class Resume(ResumeBase):
    id: int

    class Config:
        from_attributes = True
