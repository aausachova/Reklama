from src.postgre_module.repository import CandidateRepository
from .models import CreateCandidateRequest, CandidateResponse
from uuid import UUID


class CandidateService():
    def __init__(self, candidate_repository: CandidateRepository):
        self.candidate_repository = candidate_repository

    async def create_candidate(self, data: CreateCandidateRequest) -> CandidateResponse:
        candidate = await self.candidate_repository.create(**data.model_dump())
        return CandidateResponse.model_validate(candidate, from_attributes=True)

    async def get_candidate(self, candidate_id: UUID) -> CandidateResponse | None:
        candidate = await self.candidate_repository.get_by_id(candidate_id)
        if candidate:
            return CandidateResponse.model_validate(candidate, from_attributes=True)
        return None

    async def get_all_candidates(self) -> list[CandidateResponse]:
        candidates = await self.candidate_repository.get_all()
        return [CandidateResponse.model_validate(c, from_attributes=True) for c in candidates]

    async def update_candidate_status(self, candidate_id: UUID, status: str) -> CandidateResponse | None:
        candidate = await self.candidate_repository.update_status(candidate_id, status)
        if candidate:
            return CandidateResponse.model_validate(candidate, from_attributes=True)
        return None

