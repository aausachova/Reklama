from pydantic import BaseModel, EmailStr
from uuid import UUID


class CreateCandidateRequest(BaseModel):
    full_name: str
    direction: str
    phone: str
    email: EmailStr


class CandidateResponse(BaseModel):
    id: UUID
    full_name: str
    direction: str
    phone: str
    email: EmailStr
    status: str

    class Config:
        orm_mode = True

