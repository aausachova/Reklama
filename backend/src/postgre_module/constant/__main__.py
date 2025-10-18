from . import *
import asyncio
from .vacancies import create_vacancies


async def init_constants():
    # await create_roles()
    await create_vacancies()

if __name__ == "__main__":
    asyncio.run(init_constants())
