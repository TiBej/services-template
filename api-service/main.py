import logging
import os

from common.logging.otel_logger import OtelLogger
from common.rabbitmq.rabbitmq import RabbitMQ
from fastapi import FastAPI

from api.middlewares.logging_mw import logging_mw
from api.routers import users

otel_logger = OtelLogger(
    service_environment=os.getenv("SERVICE_ENVIRONMENT", "development"),
    service_name=os.getenv("SERVICE_NAME", "api-service"),
    otel_host=os.getenv("OTEL_HOST", "localhost"),
    otel_port=int(os.getenv("OTEL_PORT", 4317)),
)
handler = otel_logger.get_handler()

rabbitmq = RabbitMQ(
    service_name=os.getenv("SERVICE_NAME", "api-service"),
    user=os.getenv("RABBITMQ_USER", "admin"),
    password=os.getenv("RABBITMQ_PASSWORD", "admin"),
    host=os.getenv("RABBITMQ_HOST", "localhost"),
    port=int(os.getenv("RABBITMQ_PORT", 5672)),
)

logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(handler)

app = FastAPI(title="api-service")

# Register RabbitMQ as a dependency
app.dependency_overrides[RabbitMQ] = lambda: rabbitmq


def get_rabbitmq() -> RabbitMQ:
    return rabbitmq


app.include_router(users.router)
app.middleware("http")(logging_mw)
