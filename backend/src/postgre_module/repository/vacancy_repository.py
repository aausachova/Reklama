from uuid import UUID
from ..models import Vacancy
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class VacancyRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: UUID) -> Vacancy | None:
        stmt = select(Vacancy).where(Vacancy.id == id)
        return await self.session.scalar(stmt)

    async def create(self, title: str, city: str, company: str, type: str, direction: str, experience: bool) -> Vacancy:
        vacancy = Vacancy(title=title, city=city, company=company, type=type, direction=direction, experience=experience)
        self.session.add(vacancy)
        await self.session.flush()
        return vacancy

    async def get_all(self, company: str | None, direction: str | None, type: str | None) -> list[Vacancy]:
        stmt = select(Vacancy)
        if company and company != "all":
            stmt = stmt.where(Vacancy.company == company)
        if direction and direction != "all":
            stmt = stmt.where(Vacancy.direction == direction)
        if type and type != "all":
            stmt = stmt.where(Vacancy.type == type)
        result = await self.session.execute(stmt)
        return result.scalars().all()
