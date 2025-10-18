from fastapi import APIRouter
from .auth.controller import AuthController
from .vacancy.controller import VacancyController
from .candidate.controller import CandidateController
from .resume.controller import ResumeController

router = APIRouter(
    prefix="/api",
)

controllers = [
    AuthController,
    VacancyController,
    CandidateController,
    ResumeController
]

for controller in controllers:
    router.include_router(controller.create_router())
