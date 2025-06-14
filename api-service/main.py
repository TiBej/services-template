import logging

from common.utilities.logging_fw import LoggingFW
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
