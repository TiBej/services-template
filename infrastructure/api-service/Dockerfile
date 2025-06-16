FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY common ./common
COPY api-service ./api-service
WORKDIR /app/api-service

RUN pip install uv
RUN uv sync --frozen --no-cache

CMD ["uv", "run", "fastapi", "run", "main.py", "--port", "5001"]
