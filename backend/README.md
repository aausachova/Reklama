# Reklama Backend

Production-ready FastAPI backend with PostgreSQL, Redis, and Alembic migrations. With uv for fast Python env/package management and Docker Compose.

- API docs: http://localhost:8000/api/docs
- App entrypoint: `src.backend.app:app`

## Tech stack
- FastAPI + Uvicorn
- PostgreSQL + Alembic (migrations)
- Redis
- uv (env/package manager)
- Docker Compose

## Prerequisites
- Python 3.13+
- uv
- Docker + Docker Compose (optional, for containerized run)
- PostgreSQL, Redis (locally or via Docker (can be run via `docker-compose.yaml`))

## Quickstart (local via uv)

Install uv:
- macOS/Linux:
```bash
curl -Ls https://astral.sh/uv/install.sh | bash
```
- Windows (PowerShell):
```powershell
iwr https://astral.sh/uv/install.ps1 -UseBasicParsing | iex
```

Create env (if you want to use .bash files - it should be specifically **.env**) and install:
```bash
uv sync
```

## Database migrations

- Windows (script):
```bat
migrate.bat
```

- Manual (any OS):
```bash
alembic revision --autogenerate -m "automatic migration"
alembic upgrade head
```

## Run the app

- Windows (script):
```bat
start.bat
```

- Manual (any OS):
```bash
uvicorn src.backend.app:app --reload
```

Once running:
- Swagger UI: http://localhost:8000/api/docs

## Quickstart (Docker)

Build and start:
```bash
docker compose up --build -d
```

Stop:
```bash
docker compose down
```

## Configuration

Configuration is read from `config.toml` and environment variables. Example `.env`:

```env
POSTGRES_DB=reklama
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_USER=default
REDIS_PASSWORD=default

OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_PROVIDER=openai
OPENAI_MODEL_NAME=gpt-5

SERVER_HOST=localhost
SERVER_PORT=8000
```

Place your `.env` in the project root or where your process manager expects it. If using Docker Compose, ensure the service picks it up (env_file or environment section).