from fastapi import APIRouter
from .auth.controller import AuthController
from .vacancy.controller import VacancyController
from .resume.controller import ResumeController

router = APIRouter(
    prefix="/api",
)

router.include_router(AuthController.create_router())
router.include_router(VacancyController.create_router())
router.include_router(ResumeController.create_router())