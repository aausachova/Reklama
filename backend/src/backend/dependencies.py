from typing import Annotated
from fastapi import Request, Depends

from src.domain.services import UserService, VacancyService
from src.postgre_module.engine import DatabaseSessionManager
from src.postgre_module.repository import UserRepository, PermissionRepository, RoleRepository, VacancyRepository
from src.redis_module import RedisSessionManager
from src.redis_module import RedisRepository

from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

import logging

logger = logging.getLogger(__name__)


async def get_db_session(request: Request):
    if not hasattr(request.app.state, "postgres_manager"):
        logger.error("postgres_manager not found in app.state")
        raise RuntimeError("Database session manager not configured")
    postgres_manager: DatabaseSessionManager = request.app.state.postgres_manager
    async with postgres_manager.session() as session:
        yield session


async def get_redis_session(request: Request):
    if not hasattr(request.app.state, "redis_manager"):
        logger.error("redis_manager not found in app.state")
        raise RuntimeError("Redis session manager not configured")
    redis_manager: RedisSessionManager = request.app.state.redis_manager
    async with redis_manager.client() as redis:
        yield redis


def get_user_repository(session: Annotated[AsyncSession, Depends(get_db_session)]):
    return UserRepository(session)


def get_permission_repository(session: Annotated[AsyncSession, Depends(get_db_session)]):
    return PermissionRepository(session)


def get_role_repository(session: Annotated[AsyncSession, Depends(get_db_session)]):
    return RoleRepository(session)


def get_vacancy_repository(session: Annotated[AsyncSession, Depends(get_db_session)]):
    return VacancyRepository(session)


def get_redis_repository(redis: Annotated[Redis, Depends(get_redis_session)]):
    return RedisRepository(redis)


def get_user_service(user_repository=Depends(get_user_repository),
                     redis_repository=Depends(get_redis_repository),
                     role_repository=Depends(get_role_repository),
                     ):
    return UserService(user_repository,
                       redis_repository,
                       role_repository)


def get_vacancy_service(vacancy_repository=Depends(get_vacancy_repository)):
    return VacancyService(vacancy_repository)


UserServiceDepends = Annotated[UserService, Depends(get_user_service)]
VacancyServiceDepends = Annotated[VacancyService, Depends(get_vacancy_service)]
