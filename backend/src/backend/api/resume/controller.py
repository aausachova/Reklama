from src.backend.api.resume.models import ScoredVacancyResponse
from src.backend.dependencies import ResumeMatchingServiceDepends
from fastapi import File, UploadFile
from fastapi_controllers import Controller, post


class ResumeController(Controller):
    prefix = "/resume"
    tags = ["resume"]

    def __init__(self, resume_service: ResumeMatchingServiceDepends) -> None:
        super().__init__()
        self.resume_service = resume_service

    @post("/candidates", response_model=list[ScoredVacancyResponse])
    async def create_vacancy(self, resume_pdf: UploadFile = File(...)):
        best_vacancies = await self.resume_service.find_best_vacancies(await resume_pdf.read(), top_n=10)
        return best_vacancies
