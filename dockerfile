FROM python:3.13-alpine3.21
ARG SERVICE_NAME

WORKDIR /app

COPY common-lib ./common-lib
COPY ${SERVICE_NAME} ./${SERVICE_NAME}
WORKDIR /app/${SERVICE_NAME}

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

CMD ["poetry", "run", "start"]
