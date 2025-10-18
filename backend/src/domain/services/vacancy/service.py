from src.postgre_module.repository import VacancyRepository
from .models import CreateVacancyRequest, VacancyResponse
from uuid import UUID


class VacancyService():
    def __init__(self, vacancy_repository: VacancyRepository):
        self.vacancy_repository = vacancy_repository

    async def create_vacancy(self, data: CreateVacancyRequest) -> VacancyResponse:
        vacancy = await self.vacancy_repository.create(**data.model_dump())
        return VacancyResponse.model_validate(vacancy, from_attributes=True)

    async def get_vacancy(self, vacancy_id: UUID) -> VacancyResponse | None:
        vacancy = await self.vacancy_repository.get_by_id(vacancy_id)
        if vacancy:
            return VacancyResponse.model_validate(vacancy, from_attributes=True)
        return None

    async def get_all_vacancies(self, company: str | None, direction: str | None, type: str | None) -> list[VacancyResponse]:
        vacancies = await self.vacancy_repository.get_all(company, direction, type)
        return [VacancyResponse.model_validate(v, from_attributes=True) for v in vacancies]

    async def get_filters(self) -> dict[str, list[str]]:
        return await self.vacancy_repository.get_filters()
