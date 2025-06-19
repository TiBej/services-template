FROM python:3.13.5-slim-bookworm

ENV PYTHONUNBUFFERED=True
WORKDIR /workspace

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

COPY pyproject.toml uv.lock /workspace/
RUN uv sync --no-dev --frozen --no-install-workspace --package=api-service

COPY . /workspace
RUN uv sync --no-dev --frozen --package=api-service

CMD ["/workspace/.venv/bin/python", "/workspace/api-service", "fastapi", "run", "main.py", "--port", "5001"]
