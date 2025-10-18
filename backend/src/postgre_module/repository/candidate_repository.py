from uuid import UUID
from ..models import Candidate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class CandidateRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: UUID) -> Candidate | None:
        stmt = select(Candidate).where(Candidate.id == id)
        return await self.session.scalar(stmt)

    async def create(self, full_name: str, direction: str, phone: str, email: str, status: str) -> Candidate:
        candidate = Candidate(full_name=full_name, direction=direction, phone=phone, email=email, status=status)
        self.session.add(candidate)
        await self.session.flush()
        return candidate

    async def get_all(self) -> list[Candidate]:
        stmt = select(Candidate)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_status(self, id: UUID, status: str) -> Candidate | None:
        candidate = await self.get_by_id(id)
        if candidate:
            candidate.status = status
            await self.session.flush()
        return candidate

