from uuid import UUID

from pydantic import BaseModel


class ScoredVacancyResponse(BaseModel):
    id: UUID
    title: str
    city: str
    company: str
    type: str
    direction: str
    experience: bool
    score: float
    class Config:
        orm_mode = True