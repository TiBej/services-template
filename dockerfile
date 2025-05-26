# Use the official Python image.
FROM python:3.13-alpine3.21

# Set the working directory in the container.
WORKDIR /app

COPY example-service ./example-service
COPY common-lib ./common-lib
WORKDIR /app/example-service

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
RUN poetry run start
