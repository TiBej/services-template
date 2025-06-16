from common.logging.logging_setup import setup_logging
from common.rabbitmq.rabbitmq import RabbitMQ
from common.rabbitmq.rabbitmq_setup import setup_rabbitmq
from fastapi import FastAPI

from api.middlewares.logging_mw import logging_mw
from api.routers import users

setup_logging()
rabbitmq = setup_rabbitmq()

app = FastAPI()
app.dependency_overrides[RabbitMQ] = lambda: rabbitmq

app.include_router(users.router)
app.middleware("http")(logging_mw)
