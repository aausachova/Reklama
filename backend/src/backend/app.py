from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.backend.api import router
from src.redis_module import RedisSessionManager
from src.postgre_module import DatabaseSessionManager
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from src import env


@asynccontextmanager
async def lifespan(app: FastAPI):
    session_manager = DatabaseSessionManager(env.postgres.url)
    redis_engine = RedisSessionManager(env.redis.url)

    # Expose managers for DI functions in src.dependency
    app.state.postgres_manager = session_manager
    app.state.redis_manager = redis_engine
    yield
    if await session_manager.opened:
        await session_manager.close()
    if await redis_engine.opened:
        await redis_engine.close()


app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    title='Reklama',
    version="0.1",
    middleware=[
        Middleware(CORSMiddleware,
                   allow_origins=[
                       "localhost:8000", "26.222.166.167:8000", "26.222.166.167", "localhost"],
                   allow_methods=["*"],
                   allow_headers=["*"],
                   allow_credentials=True)
    ],
    lifespan=lifespan
)

app.include_router(router)
