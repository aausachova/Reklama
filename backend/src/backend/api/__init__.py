from fastapi import APIRouter
from .auth.controller import AuthController
from .vacancy.controller import VacancyController

router = APIRouter(
    prefix="/api",
)

router.include_router(AuthController.create_router())
router.include_router(VacancyController.create_router())
