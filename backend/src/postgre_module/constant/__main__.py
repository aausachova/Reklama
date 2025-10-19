from . import *
import asyncio
from .vacancies import create_vacancies
from .candidate import create_candidates


async def init_constants():
    await create_roles()
    await create_vacancies()
    await create_candidates()

if __name__ == "__main__":
    asyncio.run(init_constants())
