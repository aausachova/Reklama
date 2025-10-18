from . import *
import asyncio


async def init_constants():
    await create_roles()

if __name__ == "__main__":
    asyncio.run(init_constants())
