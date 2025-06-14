import logging
import threading

from common.models.events.mail_triggered import MailTriggeredEvent
from common.utilities.logging_fw import LoggingFW
from common.utilities.rabbitmq import RabbitMQ
from fastapi import FastAPI

from api.middlewares.logging_mw import logging_mw
from api.routers import users

logFW = LoggingFW(service_name="api-service")
handler = logFW.setup_logging()
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(handler)

app = FastAPI(title="api-service")


app.include_router(users.router)
app.middleware("http")(logging_mw)


def wrapped():
    def f(event: MailTriggeredEvent):
        raise Exception("Test Exception")

    rabbitMQ = RabbitMQ()
    rabbitMQ.consume(MailTriggeredEvent, f)
    pass


threading.Thread(target=wrapped).start()
