import asyncio
from types import CoroutineType
from ..engine import DatabaseSessionManager
from ..repository.permission_repository import PermissionRepository
from ..repository.role_repository import RoleRepository
from src import env
from typing import Coroutine, Any


async def create_roles():
    sessionmanager = DatabaseSessionManager(env.postgres.url)
    async with sessionmanager.session() as session:
        role_repository = RoleRepository(session)
        permission_repository = PermissionRepository(session)

        to_create: list[Coroutine[Any, Any, Any]] = []
        to_create.append(role_repository.create("resident", False))
        to_create.append(role_repository.create("curator", False))
        to_create.append(role_repository.create("moderator", False))

        await asyncio.gather(*to_create)

        to_create: list[CoroutineType] = []

        await asyncio.gather(*to_create)
