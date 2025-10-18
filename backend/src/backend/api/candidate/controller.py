from src.backend.dependencies import get_candidate_service
from src.domain.services.candidate import CandidateService
from fastapi import Depends
from typing import Annotated
from fastapi_controllers import Controller, get, post, patch
from .models import CreateCandidateRequest, CandidateResponse, UpdateCandidateStatusRequest
from uuid import UUID


class CandidateController(Controller):
    prefix = "/candidate"
    tags = ["candidate"]

    def __init__(self, candidate_service: Annotated[CandidateService, Depends(get_candidate_service)]) -> None:
        super().__init__()
        self.candidate_service = candidate_service

    @post("/", response_model=CandidateResponse)
    async def create_candidate(self, data: CreateCandidateRequest):
        return await self.candidate_service.create_candidate(data)

    @get("/{candidate_id}", response_model=CandidateResponse)
    async def get_candidate(self, candidate_id: UUID):
        return await self.candidate_service.get_candidate(candidate_id)

    @get("/", response_model=list[CandidateResponse])
    async def get_all_candidates(self):
        return await self.candidate_service.get_all_candidates()

    @patch("/{candidate_id}/status", response_model=CandidateResponse)
    async def update_candidate_status(self, candidate_id: UUID, data: UpdateCandidateStatusRequest):
        return await self.candidate_service.update_candidate_status(candidate_id, data.status)

