FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir setuptools wheel

# Копируем pyproject и src
WORKDIR /app
COPY pyproject.toml ./
COPY src ./src

RUN pip install --no-cache-dir .

WORKDIR /app/src

# Открываем порт
EXPOSE 80

# Запуск uvicorn напрямую, как в команде astral-uv
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "80"]