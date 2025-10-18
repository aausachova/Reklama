from pydantic import BaseModel
from uuid import UUID


class CreateVacancyRequest(BaseModel):
    title: str
    city: str
    company: str
    type: str
    direction: str
    experience: bool


class VacancyResponse(BaseModel):
    id: UUID
    title: str
    city: str
    company: str
    type: str
    direction: str
    experience: bool

    class Config:
        orm_mode = True


class VacancyFiltersResponse(BaseModel):
    city: list[str]
    company: list[str]
    type: list[str]
    direction: list[str]
