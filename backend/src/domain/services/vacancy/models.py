from pydantic import BaseModel, field_validator
from uuid import UUID


class CreateVacancyRequest(BaseModel):
    title: str
    city: str
    company: str
    type: str
    direction: str
    experience: bool


class UpdateVacancyRequest(BaseModel):
    active: bool


class VacancyResponse(BaseModel):
    id: UUID
    title: str
    city: str
    company: str
    type: str
    direction: str
    experience: bool
    active: bool

    class Config:
        from_attributes = True

    @field_validator("active", mode="before")
    @classmethod
    def validate_active(cls, v):
        return bool(v)

