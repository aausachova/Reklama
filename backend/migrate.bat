uv run --env-file .\.env alembic revision --autogenerate -m "automatic migration"
uv run --env-file .\.env alembic upgrade head

