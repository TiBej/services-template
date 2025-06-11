import logging

from common.utilities.logging_fw import LoggingFW
from fastapi import FastAPI

from routers import users

logFW = LoggingFW(service_name="first-service")
handler = logFW.setup_logging()
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(handler)

app = FastAPI(title="first-service")

app.include_router(users.router)
