FROM python:3.13-alpine3.21
ARG SERVICE_NAME

WORKDIR /app

COPY common ./common
COPY consumer-service ./consumer-service
WORKDIR /app/consumer-service

RUN pip install uv
RUN uv sync

CMD ["uv", "run", "main.py"]
