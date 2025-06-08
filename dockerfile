FROM python:3.13-alpine3.21
ARG SERVICE_NAME

WORKDIR /app

COPY common ./common
COPY ${SERVICE_NAME} ./${SERVICE_NAME}
WORKDIR /app/${SERVICE_NAME}

RUN pip install uv
RUN uv sync

CMD ["uv", "run", "main.py"]
