from api.middlewares.logging_mw import logging_mw
from api.routers import users
from fastapi import FastAPI

# from common.logging.logging_setup import setup_logging
from common.config.base_config import BaseConfig
from common.logging.logging_setup import setup_logging
from common.rabbitmq.rabbitmq import RabbitMQ

config = BaseConfig()
setup_logging(config)
rabbitmq = RabbitMQ(config)

app = FastAPI()
app.dependency_overrides[RabbitMQ] = lambda: rabbitmq

app.include_router(users.router)
app.middleware("http")(logging_mw)
