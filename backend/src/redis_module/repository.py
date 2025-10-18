from src.env_config import env
from redis.asyncio import Redis
from typing import Optional
from datetime import timedelta
from uuid import UUID
from .models import SessionData


class RedisRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def _get_element_by_key(self, key: str) -> SessionData | None:
        response = await self.redis.get(key)
        if not response:
            return None
        response = response.decode() if isinstance(response, bytes) else response
        return SessionData.model_validate_json(response)

    async def get_user_by_cookie(self, cookie: str) -> UUID | None:
        hash_value = f"cookie::{cookie}"
        session_data = await self._get_element_by_key(hash_value)
        if not session_data:
            return None
        return session_data.user_id

    async def get_session_data_cookie(self, cookie: str) -> SessionData | None:
        hash_value = f"cookie::{cookie}"
        session_data = await self._get_element_by_key(hash_value)
        if not session_data:
            return None
        return session_data


    async def _extend_user_set(self, user_id: UUID, token: str) -> None:
        key = f"user::session::{user_id}"
        await self.redis.sadd(key, token)  # type: ignore

    async def _remove_from_user_set(self, user_id: UUID, token: str) -> None:
        key = f"user::session::{user_id}"
        await self.redis.srem(key, token)  # type: ignore

    async def set_user_cookie(self, token: str, session_data: SessionData, expire: timedelta = timedelta(days=30)) -> None:
        key = f"cookie::{token}"
        await self.redis.set(key, session_data.model_dump_json(), ex=expire)
        await self._extend_user_set(session_data.user_id, token)

    async def remove_user_cookie(self, token: str) -> None:
        user_uuid = await self.get_user_by_cookie(token)
        if not user_uuid:
            return
        key = f"cookie::{token}"
        await self.redis.delete(key)
        await self._remove_from_user_set(user_uuid, token)

    async def get_all_user_cookies(self, user_id: UUID) -> list[str]:
        key = f"user::session::{user_id}"
        tokens = await self.redis.smembers(key)  # type: ignore
        if not tokens:
            return []
        return [token.decode() if isinstance(token, bytes) else token for token in tokens]

    async def revoke_all_user_cookies(self, user_id: UUID, exclude_token: None | str | list[str] = None) -> None:
        key = f"user::session::{user_id}"
        tokens = await self.redis.smembers(key)  # type: ignore
        if not tokens:
            return
        tokens_to_delete = []
        for token in tokens:
            token_str = token.decode() if isinstance(token, bytes) else token
            if (
                    exclude_token is None or
                    (isinstance(exclude_token, str) and token_str != exclude_token) or
                    (isinstance(exclude_token, list) and token_str not in exclude_token)
            ):
                tokens_to_delete.append(token_str)
        if tokens_to_delete:
            await self.redis.delete(*[f"cookie::{token}" for token in tokens_to_delete])
            if exclude_token is None:
                await self.redis.delete(key)
            else:
                await self.redis.srem(key, *tokens_to_delete)  # type: ignore
