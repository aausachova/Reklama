from uuid import UUID
from ..models import Vacancy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional


class VacancyRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: UUID) -> Vacancy | None:
        stmt = select(Vacancy).where(Vacancy.id == id)
        return await self.session.scalar(stmt)

    async def create(self, title: str, city: str, company: str, type: str, direction: str, experience: bool,
                     requirements: list[str] = [], skills: list[str] = []) -> Vacancy:
        vacancy = Vacancy(title=title, city=city, company=company, type=type, direction=direction,
                          experience=experience, requirements=requirements, skills=skills)
        self.session.add(vacancy)
        await self.session.flush()
        return vacancy

    async def get_all(
            self,
            company: Optional[str] = None,
            direction: Optional[str] = None,
            type: Optional[str] = None
    ) -> list[Vacancy]:
        stmt = select(Vacancy)

        if company and company.lower() != "all":
            stmt = stmt.where(func.lower(Vacancy.company) == company.lower())
        if direction and direction.lower() != "all":
            stmt = stmt.where(func.lower(Vacancy.direction) == direction.lower())
        if type and type.lower() != "all":
            stmt = stmt.where(func.lower(Vacancy.type) == type.lower())

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, vacancy: Vacancy, data: dict) -> Vacancy:
        for key, value in data.items():
            setattr(vacancy, key, value)
        await self.session.flush()
        return vacancy

    async def delete(self, vacancy: Vacancy) -> None:
        await self.session.delete(vacancy)
        await self.session.flush()

    async def get_filters(self) -> dict[str, list[str]]:
        city_stmt = select(Vacancy.city).distinct()
        company_stmt = select(Vacancy.company).distinct()
        type_stmt = select(Vacancy.type).distinct()
        direction_stmt = select(Vacancy.direction).distinct()

        cities = await self.session.execute(city_stmt)
        companies = await self.session.execute(company_stmt)
        types = await self.session.execute(type_stmt)
        directions = await self.session.execute(direction_stmt)

        return {
            "city": cities.scalars().all(),
            "company": companies.scalars().all(),
            "type": types.scalars().all(),
            "direction": directions.scalars().all(),
        }
