FROM python:3.13-slim

WORKDIR /

COPY pyproject.toml ./

RUN pip install --upgrade pip
RUN pip install uv
RUN uv pip install --system --editable .

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "alembic revision --autogenerate && alembic upgrade head && ./start.bat"]