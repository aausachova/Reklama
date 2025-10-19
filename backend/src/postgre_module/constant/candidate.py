import asyncio
import json
from pathlib import Path
from src import env
from src.postgre_module.engine import DatabaseSessionManager
from src.postgre_module.repository.candidate_repository import CandidateRepository
from src.postgre_module.models import Candidate


async def create_candidates():
    sessionmanager = DatabaseSessionManager(env.postgres.url)
    json_path = Path(__file__).parent / "candidates.json"

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            candidates_data = json.load(f)
    except FileNotFoundError:
        print(f"Candidate data file not found at {json_path}. Skipping candidate creation.")
        return

    valid_fields = {col.name for col in Candidate.__table__.columns}

    async with sessionmanager.session() as session:
        candidate_repository = CandidateRepository(session)

        for candidate_data in candidates_data:
            filtered_data = {
                k: v for k, v in candidate_data.items()
                if k in valid_fields and k != "id"
            }

            try:
                await candidate_repository.create(**filtered_data)
            except Exception as e:
                print(f"Failed to insert candidate '{candidate_data.get('full_name')}': {e}")

        await session.commit()

    print(f"Imported {len(candidates_data)} candidates (extra fields ignored).")


if __name__ == "__main__":
    asyncio.run(create_candidates())
