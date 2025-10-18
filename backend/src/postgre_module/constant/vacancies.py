import asyncio
import json
from pathlib import Path
from src import env
from src.postgre_module.engine import DatabaseSessionManager
from src.postgre_module.repository.vacancy_repository import VacancyRepository
from src.postgre_module.models import Vacancy


async def create_vacancies():
    sessionmanager = DatabaseSessionManager(env.postgres.url)
    json_path = Path(__file__).parent / "vacancies.json"

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            vacancies_data = json.load(f)
    except FileNotFoundError:
        print(f"Vacancy data file not found at {json_path}. Skipping vacancy creation.")
        return

    valid_fields = {col.name for col in Vacancy.__table__.columns}

    async with sessionmanager.session() as session:
        vacancy_repository = VacancyRepository(session)

        for vacancy_data in vacancies_data:
            filtered_data = {
                k: v for k, v in vacancy_data.items() if k in valid_fields and k != "id"
            }

            try:
                await vacancy_repository.create(**filtered_data)
            except Exception as e:
                print(f"Failed to insert vacancy '{vacancy_data.get('title')}' ({vacancy_data.get('company')}): {e}")
        await session.commit()
    print(f"Imported {len(vacancies_data)} vacancies (extra fields ignored).")


if __name__ == "__main__":
    asyncio.run(create_vacancies())
