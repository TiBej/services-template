import logging

from fastapi import FastAPI
from routers import users

from common.utilities.logging_fw import LoggingFW

logFW = LoggingFW(service_name="api-service")
handler = logFW.setup_logging()
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(handler)

app = FastAPI(title="api-service")

app.include_router(users.router)
