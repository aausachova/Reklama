from src.backend.dependencies import get_vacancy_service
from src.domain.services import VacancyService
from fastapi import Depends
from typing import Annotated
from fastapi_controllers import Controller, get, post
from .models import CreateVacancyRequest, VacancyResponse, VacancyFiltersResponse
from uuid import UUID


class VacancyController(Controller):
    prefix = "/vacancy"
    tags = ["vacancy"]

    def __init__(self, vacancy_service: Annotated[VacancyService, Depends(get_vacancy_service)]) -> None:
        super().__init__()
        self.vacancy_service = vacancy_service

    @post("/", response_model=VacancyResponse)
    async def create_vacancy(self, data: CreateVacancyRequest):
        return await self.vacancy_service.create_vacancy(data)

    @get("/{vacancy_id}", response_model=VacancyResponse)
    async def get_vacancy(self, vacancy_id: UUID):
        return await self.vacancy_service.get_vacancy(vacancy_id)

    @get("/", response_model=list[VacancyResponse])
    async def get_all_vacancies(self, company: str | None = None, direction: str | None = None, type: str | None = None):
        return await self.vacancy_service.get_all_vacancies(company, direction, type)

    @get("/filters", response_model=VacancyFiltersResponse)
    async def get_filters(self):
        return await self.vacancy_service.get_filters()
